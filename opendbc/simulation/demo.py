#!/usr/bin/env python3
"""
Prototype demo: virtual vehicle + ESP32-style security gateway (no real car).

Run from repo root (after pip install -e .):
  python -m opendbc.simulation.demo
"""

from __future__ import annotations

import sys
import time

from opendbc.simulation.auth import AuthEngine, KeyPair
from opendbc.simulation.can_bus import CANBus, CANFrame
from opendbc.simulation.gateway import GatewayDecision, SecurityGateway
from opendbc.simulation.protocol import MsgId
from opendbc.simulation.threats import ThreatSimulator
from opendbc.simulation.vehicle import FakeVehicleSimulator


def banner(title: str) -> None:
  print()
  print("=" * 60)
  print(f"  {title}")
  print("=" * 60)


def ok(label: str, passed: bool) -> None:
  status = "PASS" if passed else "FAIL"
  print(f"  [{status}] {label}")


def main() -> int:
  bus = CANBus()
  auth = AuthEngine()
  client_keys = KeyPair.generate()
  vehicle = FakeVehicleSimulator(bus)
  gateway = SecurityGateway(bus, auth, client_keys.public_key)
  threats = ThreatSimulator(gateway, KeyPair.generate())

  banner("1. Authentication — challenge / response / session")
  session, msg = gateway.authenticate_client(client_keys)
  ok("User signs nonce, gateway verifies", session is not None)
  print(f"       Gateway says: {msg}")
  if session:
    print(f"       Session token: {session.token[:24]}... (expires in 300s)")

  banner("2. Fake vehicle simulator — telemetry")
  vehicle.set_ignition(True)
  for _ in range(5):
    vehicle.tick(0.2)
    time.sleep(0.05)
  snap = vehicle.snapshot()
  print(f"       RPM={snap['rpm']}  speed={snap['speed_kph']} kph  ignition={snap['ignition']}")
  print(f"       ECUs online: {[k for k, v in snap['ecus'].items() if v]}")
  ok("Vehicle broadcasting CAN state", snap["rpm"] > 0)

  banner("3. Security gateway — safe vs dangerous CAN")
  rid = SecurityGateway.new_request_id()
  door = gateway.send_can(CANFrame(MsgId.DOOR_CMD, b"\x01"), request_id=rid)
  ok("Safe request (door lock) forwarded", door.decision == GatewayDecision.ALLOW)

  steer_blocked = gateway.send_can(
    CANFrame(MsgId.STEER_CMD, b"\x20\x00"),
    request_id=SecurityGateway.new_request_id(),
  )
  ok("Dangerous steer blocked without controls_allowed", steer_blocked.decision == GatewayDecision.BLOCK_DANGEROUS)
  print(f"       {steer_blocked.message}")

  gateway.enable_controls()
  steer_ok = gateway.send_can(
    CANFrame(MsgId.STEER_CMD, b"\x20\x00"),
    request_id=SecurityGateway.new_request_id(),
  )
  ok("Steer allowed after auth + controls_allowed", steer_ok.decision == GatewayDecision.ALLOW)
  vehicle.tick(0.1)
  print(f"       Speed after steer: {vehicle.snapshot()['speed_kph']} kph")

  banner("4. Threat simulation")
  t1 = threats.unauthorized_access()
  ok(t1["attack"], t1["blocked"])
  print(f"       {t1['detail']}")

  # Re-auth for replay demo
  gateway.authenticate_client(client_keys)
  gateway.enable_controls()
  replay_id = SecurityGateway.new_request_id()
  gateway.send_can(CANFrame(MsgId.DOOR_CMD, b"\x00"), request_id=replay_id)
  assert gateway.session is not None
  t2 = threats.replay_attack(replay_id, gateway.session.token)
  ok(t2["attack"], t2["blocked"])
  print(f"       {t2['detail']}")

  t3 = threats.can_injection()
  ok("CAN injection (unknown ID)", t3["unknown_id_blocked"])
  ok("CAN injection (fake session actuation)", t3["actuation_blocked"])
  print(f"       Unknown: {t3['unknown_detail']}")
  print(f"       Actuation: {t3['actuation_detail']}")

  t4 = threats.wrong_key_auth()
  ok("Wrong key rejected", t4["blocked"])
  print(f"       {t4['detail']}")

  banner("Audit log (last 6 gateway decisions)")
  for entry in gateway.audit_log()[-6:]:
    print(f"       {entry.decision.value:20s} — {entry.message}")

  banner("Demo complete")
  print("  No hardware required. Stack: auth + fake CAN + gateway firewall + threats.")
  print()
  return 0


if __name__ == "__main__":
  sys.exit(main())
