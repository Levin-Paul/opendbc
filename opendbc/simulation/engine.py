"""Simulation engine for dashboard API — auth, gateway, vehicle, threats, OpenDBC."""

from __future__ import annotations

import asyncio
import secrets
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

from opendbc.simulation.auth import AuthEngine, KeyPair
from opendbc.simulation.can_bus import CANBus, CANFrame
from opendbc.simulation.gateway import GatewayDecision, SecurityGateway
from opendbc.simulation.opendbc_bridge import OpenDBCBridge
from opendbc.simulation.profiles import DEFAULT_PROFILE_ID, PROFILES, VehicleProfile
from opendbc.simulation.protocol import MsgId
from opendbc.simulation.threats import ThreatSimulator
from opendbc.simulation.vehicle import FakeVehicleSimulator


class AuthState(str, Enum):
  DISCONNECTED = "disconnected"
  AUTHENTICATING = "authenticating"
  VERIFIED = "verified"
  BLOCKED = "blocked"
  EXPIRED = "expired"


class FlowState(str, Enum):
  IDLE = "idle"
  NORMAL = "normal"
  SECURE = "secure"
  SUSPICIOUS = "suspicious"
  BLOCKED = "blocked"
  LOCKDOWN = "lockdown"


@dataclass
class LogEvent:
  timestamp: str
  level: str
  message: str


FIREWALL_RULES: list[dict[str, str]] = [
  {"id": "READ_VEHICLE_SPEED", "action": "allow", "category": "read"},
  {"id": "READ_RPM", "action": "allow", "category": "read"},
  {"id": "READ_DOOR_STATUS", "action": "allow", "category": "read"},
  {"id": "READ_BATTERY", "action": "allow", "category": "read"},
  {"id": "READ_IGNITION", "action": "allow", "category": "read"},
  {"id": "READ_STEERING_ANGLE", "action": "allow", "category": "read"},
  {"id": "STEERING_ACTUATION", "action": "block", "category": "actuation"},
  {"id": "BRAKE_OVERRIDE", "action": "block", "category": "actuation"},
  {"id": "THROTTLE_OVERRIDE", "action": "block", "category": "actuation"},
  {"id": "ECU_REPROGRAMMING", "action": "block", "category": "critical"},
  {"id": "RAW_UNSIGNED_CAN_WRITE", "action": "block", "category": "critical"},
  {"id": "ENGINE_SHUTDOWN", "action": "block", "category": "critical"},
]

READ_OPS = {
  "READ_RPM": MsgId.VEHICLE_STATE,
  "READ_SPEED": MsgId.VEHICLE_STATE,
  "READ_VEHICLE_SPEED": MsgId.VEHICLE_STATE,
  "READ_DOOR_STATUS": MsgId.DOOR_STATUS,
  "READ_BATTERY": MsgId.ECU_HEARTBEAT,
  "READ_IGNITION": MsgId.VEHICLE_STATE,
  "READ_STEERING_ANGLE": MsgId.VEHICLE_STATE,
}

ACTUATION_OPS = {
  "STEERING_ACTUATION": MsgId.STEER_CMD,
  "BRAKE_OVERRIDE": MsgId.BRAKE_CMD,
  "THROTTLE_OVERRIDE": MsgId.GAS_CMD,
  "ENGINE_SHUTDOWN": MsgId.GAS_CMD,
  "ECU_REPROGRAMMING": MsgId.GAS_CMD,
  "RAW_UNSIGNED_CAN_WRITE": MsgId.STEER_CMD,
}


class SimulationEngine:
  def __init__(self) -> None:
    self.bus = CANBus()
    self.auth_engine = AuthEngine()
    self.client_keys = KeyPair.generate()
    self.attacker_keys = KeyPair.generate()
    self.vehicle = FakeVehicleSimulator(self.bus)
    self.gateway = SecurityGateway(self.bus, self.auth_engine, self.client_keys.public_key)
    self.threats = ThreatSimulator(self.gateway, self.attacker_keys)
    self.profile = PROFILES[DEFAULT_PROFILE_ID]
    self.bridge = OpenDBCBridge(self.profile)
    self._listeners: list[Callable[[dict], None]] = []
    self._events: list[LogEvent] = []
    self._request_queue: list[dict] = []
    self._defense_actions: list[dict] = []
    self._last_can_frames: list[dict] = []
    self._auth_state = AuthState.DISCONNECTED
    self._flow_state = FlowState.IDLE
    self._challenge: dict | None = None
    self._device_id = f"DEV-{secrets.token_hex(4).upper()}"
    self._presentation_mode = False
    self._privacy_mode = False
    self._demo_mode = False
    self._lockdown = False
    self._rate_limited = False
    self._tamper = False
    self._gateway_online = True
    self._active_rule: str | None = None
    self._full_demo_running = False
    self._steering_angle = 0.0
    self._battery_v = 12.6
    self._accel_pedal = 0.0
    self._brake_pressed = False
    self._cruise_on = False
    self._seatbelt = True
    self._turn_signal = "off"

  def on_broadcast(self, listener: Callable[[dict], None]) -> None:
    self._listeners.append(listener)

  def _emit(self, msg_type: str, payload: dict) -> None:
    envelope = {"type": msg_type, "payload": payload, "ts": time.time()}
    for listener in list(self._listeners):
      listener(envelope)

  def _log(self, message: str, level: str = "info") -> None:
    if self._privacy_mode and level == "info":
      return
    ev = LogEvent(time.strftime("%H:%M:%S"), level, message)
    self._events.append(ev)
    if len(self._events) > 200:
      self._events = self._events[-200:]
    self._emit("event", {"timestamp": ev.timestamp, "level": ev.level, "message": ev.message})

  def set_profile(self, profile_id: str) -> bool:
    if profile_id not in PROFILES:
      return False
    self.profile = PROFILES[profile_id]
    self.bridge = OpenDBCBridge(self.profile)
    self._log(f"Vehicle profile switched to {self.profile.label}", "blue")
    return True

  def get_state(self) -> dict[str, Any]:
    snap = self.vehicle.snapshot()
    session = self.gateway.session
    session_remaining = 0
    if session:
      session_remaining = max(0, int(session.expires_at - time.time()))

    return {
      "system_status": "LOCKDOWN" if self._lockdown else ("SECURE" if session else "STANDBY"),
      "vehicle_online": self._gateway_online,
      "session_active": session is not None,
      "session_remaining_s": session_remaining,
      "auth": {
        "state": self._auth_state.value,
        "device_id": self._device_id,
        "nonce_hex": self._challenge["nonce_hex"] if self._challenge else None,
        "challenge_id": self._challenge["challenge_id"] if self._challenge else None,
        "signature_verified": self._auth_state == AuthState.VERIFIED,
        "session_token_preview": session.token[:20] + "..." if session else None,
      },
      "gateway": {
        "controls_allowed": self.gateway.controls_allowed,
        "lockdown": self._lockdown,
        "queue": self._request_queue[-8:],
      },
      "firewall": {
        "rules": FIREWALL_RULES,
        "active_rule": self._active_rule,
        "rate_limited": self._rate_limited,
        "replay_detection": True,
        "session_validation": session is not None,
      },
      "vehicle": {
        **snap,
        "profile_id": self.profile.id,
        "profile_label": self.profile.label,
        "dbc": self.profile.dbc,
        "opendbc_available": self.bridge.available,
        "steering_angle": round(self._steering_angle, 1),
        "battery_v": round(self._battery_v, 2),
        "accel_pedal": round(self._accel_pedal, 2),
        "brake_pressed": self._brake_pressed,
        "cruise_on": self._cruise_on,
        "seatbelt": self._seatbelt,
        "turn_signal": self._turn_signal,
        "tamper": self._tamper,
        "vibration": self._tamper,
        "tilt": False,
      },
      "flow": self._flow_state.value,
      "defense": self._defense_actions[-6:],
      "events": [{"timestamp": e.timestamp, "level": e.level, "message": e.message} for e in self._events[-40:]],
      "can_frames": self._last_can_frames[-12:],
      "settings": {
        "presentation_mode": self._presentation_mode,
        "privacy_mode": self._privacy_mode,
        "demo_mode": self._demo_mode,
      },
    }

  def tick(self) -> None:
    if not self._gateway_online:
      return
    self.vehicle.tick(0.25)
    if self.vehicle.state.ignition:
      self._battery_v = max(11.8, self._battery_v - 0.001)
      self._steering_angle += (secrets.randbelow(21) - 10) * 0.1
      self._steering_angle = max(-180.0, min(180.0, self._steering_angle))
    snap = self.vehicle.snapshot()
    state = {**snap, "steering_angle": self._steering_angle, "brake_pressed": self._brake_pressed}
    self._last_can_frames = self.bridge.build_telemetry_frames(state)
    if not self._last_can_frames and self.bridge.available is False:
      self._last_can_frames = [{
        "timestamp": time.time(),
        "address": int(MsgId.VEHICLE_STATE),
        "address_hex": f"0x{int(MsgId.VEHICLE_STATE):X}",
        "data_hex": "SIMULATED",
        "message": "VEHICLE_STATE",
        "primary_signal": "SPEED",
        "decoded": [
          {"signal": "SPEED", "value": snap["speed_kph"], "unit": "km/h"},
          {"signal": "RPM", "value": snap["rpm"], "unit": "rpm"},
        ],
      }]
    self._emit("state", self.get_state())

  async def run_loop(self, interval: float = 0.4) -> None:
    while True:
      self.tick()
      await asyncio.sleep(interval)

  def connect_device(self) -> dict:
    self._auth_state = AuthState.AUTHENTICATING
    self._flow_state = FlowState.NORMAL
    self._log("Device connected", "blue")
    return {"ok": True, "device_id": self._device_id}

  def request_challenge(self) -> dict:
    ch = self.auth_engine.issue_challenge()
    self._challenge = {
      "challenge_id": ch.challenge_id,
      "nonce_hex": ch.nonce.hex(),
      "expires_at": ch.expires_at,
    }
    self._auth_state = AuthState.AUTHENTICATING
    self._log("Authentication challenge issued", "blue")
    return self._challenge

  def sign_challenge(self) -> dict:
    if not self._challenge:
      return {"ok": False, "error": "no challenge"}
    ch_id = self._challenge["challenge_id"]
    ch = self.auth_engine._challenges.get(ch_id)  # noqa: SLF001
    if ch is None:
      return {"ok": False, "error": "challenge expired — request again"}
    sig = self.client_keys.sign(ch.nonce)
    session = self.auth_engine.verify_challenge_response(
      ch_id, sig, self.client_keys.public_key, subject="authorized_client",
    )
    if session:
      self.gateway._session = session  # noqa: SLF001
      msg = "access granted"
    else:
      session = None
      msg = "signature verification failed"
    if session:
      self._auth_state = AuthState.VERIFIED
      self._flow_state = FlowState.SECURE
      self._log("Signature verified — session established", "green")
      self._defense("Session token minted", "green")
      return {"ok": True, "message": msg, "session": session.token}
    self._auth_state = AuthState.BLOCKED
    self._flow_state = FlowState.BLOCKED
    self._log(f"Authentication failed: {msg}", "red")
    return {"ok": False, "message": msg}

  def disconnect(self) -> dict:
    self.gateway.logout()
    self._auth_state = AuthState.DISCONNECTED
    self._flow_state = FlowState.IDLE
    self._challenge = None
    self._log("Device disconnected", "yellow")
    return {"ok": True}

  def revoke_session(self) -> dict:
    self.gateway.logout()
    self._auth_state = AuthState.EXPIRED
    self._flow_state = FlowState.IDLE
    self._defense("Session revoked", "yellow")
    self._log("Session revoked", "yellow")
    return {"ok": True}

  def enable_controls(self) -> dict:
    self.gateway.enable_controls()
    self._log("Controls allowed enabled (authorized actuation)", "green")
    return {"ok": True}

  def _defense(self, action: str, color: str = "green") -> None:
    entry = {"action": action, "color": color, "ts": time.time()}
    self._defense_actions.append(entry)
    self._emit("defense", entry)

  def process_request(self, operation: str) -> dict:
    self._active_rule = operation
    entry = {
      "operation": operation,
      "status": "pending",
      "ts": time.time(),
    }
    self._request_queue.append(entry)
    if len(self._request_queue) > 20:
      self._request_queue = self._request_queue[-20:]

    if self._lockdown:
      entry["status"] = "blocked"
      entry["reason"] = "gateway lockdown"
      self._log(f"{operation} blocked — LOCKDOWN", "red")
      self._flow_state = FlowState.LOCKDOWN
      return {"decision": "block", "message": "LOCKDOWN MODE ACTIVE", "operation": operation}

    rule = next((r for r in FIREWALL_RULES if r["id"] == operation), None)
    if rule and rule["action"] == "allow":
      msg_id = READ_OPS.get(operation, MsgId.VEHICLE_STATE)
      result = self.gateway.send_can(CANFrame(msg_id, b"\x00"), request_id=SecurityGateway.new_request_id())
      entry["status"] = "allowed"
      self._log(f"{operation} allowed → {self.profile.label}", "green")
      self._flow_state = FlowState.SECURE
      snap = self.vehicle.snapshot()
      value = ""
      if operation == "READ_VEHICLE_SPEED" or operation == "READ_SPEED":
        value = f"speed = {snap['speed_kph']} km/h"
      elif operation == "READ_RPM":
        value = f"RPM = {snap['rpm']}"
      return {"decision": "allow", "operation": operation, "detail": value, "gateway": result.decision.value}

    if operation in ACTUATION_OPS:
      msg_id = ACTUATION_OPS[operation]
      payload = b"\xFF" if operation != "STEERING_ACTUATION" else b"\x40\x00"
      result = self.gateway.send_can(CANFrame(msg_id, payload), request_id=SecurityGateway.new_request_id())
      blocked = result.decision != GatewayDecision.ALLOW
      entry["status"] = "blocked" if blocked else "allowed"
      if blocked:
        self._flow_state = FlowState.BLOCKED
        self._log(f"{operation} BLOCKED by CAN firewall", "red")
        self._defense(f"Blocked {operation}", "red")
        return {
          "decision": "block",
          "operation": operation,
          "message": result.message,
          "alert": f"{operation.replace('_', ' ')} BLOCKED",
        }
      self._log(f"{operation} forwarded (controls allowed)", "yellow")
      return {"decision": "allow", "operation": operation}

    entry["status"] = "blocked"
    self._log(f"Unknown operation {operation}", "red")
    return {"decision": "block", "operation": operation}

  def run_attack(self, attack_type: str) -> dict:
    self._demo_mode = True
    alerts = {
      "unauthorized": ("UNAUTHORIZED DEVICE BLOCKED", "red", self._attack_unauthorized),
      "replay": ("REPLAY ATTACK DETECTED", "red", self._attack_replay),
      "can_injection": ("ILLEGAL CAN TRAFFIC BLOCKED", "red", self._attack_can_injection),
      "ecu_flash": ("CRITICAL ECU MODIFICATION BLOCKED", "red", self._attack_ecu_flash),
      "dos": ("DOS ATTACK MITIGATED", "yellow", self._attack_dos),
      "spoofing": ("IDENTITY SPOOFING DETECTED", "red", self._attack_spoofing),
      "tampering": ("PHYSICAL TAMPERING DETECTED", "red", self._attack_tampering),
      "obd_bypass": ("UNAUTHORIZED BUS ACCESS DETECTED", "red", self._attack_obd),
      "power_cut": ("GATEWAY FAILSAFE ACTIVATED", "yellow", self._attack_power),
      "mitm": ("INTERCEPTION ATTEMPT FAILED", "green", self._attack_mitm),
    }
    if attack_type not in alerts:
      return {"ok": False, "error": "unknown attack"}
    title, color, fn = alerts[attack_type]
    result = fn()
    result["alert"] = title
    result["alert_color"] = color
    self._emit("attack", result)
    return result

  def _attack_unauthorized(self) -> dict:
    self._flow_state = FlowState.BLOCKED
    r = self.threats.unauthorized_access()
    self._log("Unauthorized device connection blocked", "red")
    self._defense("Blocked unauthorized traffic", "red")
    return r

  def _attack_replay(self) -> dict:
    self._flow_state = FlowState.BLOCKED
    if not self.gateway.session:
      self.sign_challenge()
    rid = SecurityGateway.new_request_id()
    token = self.gateway.session.token if self.gateway.session else ""
    self.gateway.send_can(CANFrame(MsgId.DOOR_CMD, b"\x01"), request_id=rid)
    r = self.threats.replay_attack(rid, token)
    self._log("Replay attack detected — nonce/request mismatch", "red")
    self._defense("Rotating session nonce", "yellow")
    return r

  def _attack_can_injection(self) -> dict:
    self._flow_state = FlowState.BLOCKED
    r = self.threats.can_injection()
    self._log("Rogue CAN injection blocked by firewall", "red")
    self._defense("Threat isolation enabled", "red")
    return r

  def _attack_ecu_flash(self) -> dict:
    self._lockdown = True
    self._flow_state = FlowState.LOCKDOWN
    r = self.process_request("ECU_REPROGRAMMING")
    self._defense("Gateway lockdown activated", "red")
    return {**r, "fullscreen": True}

  def _attack_dos(self) -> dict:
    self._rate_limited = True
    self._flow_state = FlowState.SUSPICIOUS
    for _ in range(20):
      self.gateway.send_can(CANFrame(MsgId.DOOR_CMD, b"\x00"), request_id=SecurityGateway.new_request_id())
    self._defense("Rate limiting activated", "yellow")
    self._log("DoS packet flood mitigated", "yellow")
    return {"blocked": True, "attack": "dos", "rate_limited": True}

  def _attack_spoofing(self) -> dict:
    self._flow_state = FlowState.BLOCKED
    r = self.threats.wrong_key_auth()
    self._log("Device spoofing — signature mismatch", "red")
    return r

  def _attack_tampering(self) -> dict:
    self._tamper = True
    self._lockdown = True
    self._flow_state = FlowState.LOCKDOWN
    self._log("Physical tamper sensor triggered", "red")
    self._defense("Safe mode activation", "red")
    return {"blocked": True, "attack": "tampering", "shake": True}

  def _attack_obd(self) -> dict:
    self._flow_state = FlowState.SUSPICIOUS
    r = self.gateway.send_can(
      CANFrame(0x7E0, b"\x02\x10\x03"),
      session_token=None,
      request_id=SecurityGateway.new_request_id(),
    )
    self._log("OBD port bypass attempt — anomaly detected", "yellow")
    return {"blocked": r.decision != GatewayDecision.ALLOW, "detail": r.message}

  def _attack_power(self) -> dict:
    self._gateway_online = False
    self._flow_state = FlowState.IDLE
    self._log("Gateway power loss — failsafe activated", "yellow")
    self._defense("Failsafe: CAN buses silent", "yellow")
    return {"failsafe": True}

  def _attack_mitm(self) -> dict:
    self._log("MITM intercept attempt — signature prevents replay", "green")
    return {"blocked": True, "attack": "mitm"}

  def set_ignition(self, on: bool) -> None:
    self.vehicle.set_ignition(on)
    self._log(f"Ignition {'ON' if on else 'OFF'}", "blue")

  def set_doors(self, open_doors: bool) -> None:
    s = self.vehicle.state
    s.door_fl = s.door_fr = s.door_rl = s.door_rr = open_doors
    self.vehicle._broadcast()  # noqa: SLF001
    self._log(f"Doors {'opened' if open_doors else 'closed'}", "blue")

  def disconnect_ecu(self, ecu: str) -> None:
    if ecu in self.vehicle.state.ecus:
      self.vehicle.state.ecus[ecu] = False
      self._log(f"ECU {ecu} offline", "yellow")

  def simulate_battery_drop(self) -> None:
    self._battery_v = 10.2
    self._log("Battery voltage drop simulated", "yellow")

  def reset(self) -> None:
    self.__init__()
    self._log("Demo reset", "blue")

  async def run_full_demo(self) -> None:
    if self._full_demo_running:
      return
    self._full_demo_running = True
    self._demo_mode = True
    steps = [
      ("unauthorized", None),
      ("wait", 1.2),
      ("connect", None),
      ("challenge", None),
      ("sign", None),
      ("read_rpm", "READ_RPM"),
      ("replay", None),
      ("spoofing", None),
      ("can_injection", None),
      ("ecu_flash", None),
      ("tampering", None),
      ("wait", 1.0),
      ("reset_partial", None),
    ]
    step_idx = 0
    for step in steps:
      self._emit("demo_step", {"step": step_idx, "action": step[0]})
      step_idx += 1
      if step[0] == "wait":
        await asyncio.sleep(step[1])
      elif step[0] == "connect":
        self.connect_device()
      elif step[0] == "challenge":
        self.request_challenge()
      elif step[0] == "sign":
        self.sign_challenge()
        self.enable_controls()
      elif step[0] == "read_rpm":
        self.process_request(step[1])
      elif step[0] == "reset_partial":
        self._lockdown = False
        self._tamper = False
        self._rate_limited = False
        self._gateway_online = True
      else:
        self.run_attack(step[0])
      await asyncio.sleep(1.8 if self._presentation_mode else 1.2)
    self._full_demo_running = False
    self._emit("demo_step", {"step": -1, "action": "complete"})
