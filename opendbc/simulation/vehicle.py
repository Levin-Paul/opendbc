"""Fake vehicle: RPM, speed, doors, ignition, ECU presence."""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from opendbc.simulation.can_bus import CANBus, CANFrame
from opendbc.simulation.protocol import (
  MsgId,
  pack_door_status,
  pack_ecu_heartbeat,
  pack_vehicle_state,
  unpack_door_status,
)


@dataclass
class VehicleState:
  speed_kph: float = 0.0
  rpm: int = 0
  ignition: bool = False
  door_fl: bool = False
  door_fr: bool = False
  door_rl: bool = False
  door_rr: bool = False
  trunk: bool = False
  ecus: dict[str, bool] = field(default_factory=lambda: {
    "ecm": True,
    "tcm": True,
    "abs": True,
    "eps": True,
    "bcm": True,
  })


class FakeVehicleSimulator:
  """Subscribes to CAN bus and broadcasts telemetry; applies allowed commands."""

  def __init__(self, bus: CANBus) -> None:
    self.bus = bus
    self.state = VehicleState()
    bus.subscribe(self._on_frame)
    self._last_tick = time.time()

  def tick(self, dt: float | None = None) -> None:
    """Advance physics-ish state and publish CAN frames."""
    now = time.time()
    if dt is None:
      dt = now - self._last_tick
    self._last_tick = now

    if self.state.ignition:
      target_rpm = 800 if self.state.speed_kph < 1 else 1500 + int(self.state.speed_kph * 40)
      self.state.rpm = int(self.state.rpm * 0.9 + target_rpm * 0.1)
    else:
      self.state.rpm = max(0, self.state.rpm - int(200 * dt))
      self.state.speed_kph = max(0.0, self.state.speed_kph - 5.0 * dt)

    self._broadcast()

  def _broadcast(self) -> None:
    self.bus.send(CANFrame(
      MsgId.VEHICLE_STATE,
      pack_vehicle_state(self.state.speed_kph, self.state.rpm, self.state.ignition),
    ))
    self.bus.send(CANFrame(
      MsgId.DOOR_STATUS,
      pack_door_status(
        self.state.door_fl, self.state.door_fr,
        self.state.door_rl, self.state.door_rr, self.state.trunk,
      ),
    ))
    self.bus.send(CANFrame(
      MsgId.ECU_HEARTBEAT,
      pack_ecu_heartbeat(self.state.ecus),
    ))

  def _on_frame(self, frame: CANFrame) -> None:
    if frame.arbitration_id == MsgId.DOOR_CMD and frame.data:
      lock = frame.data[0] == 1
      self.state.door_fl = lock
      self.state.door_fr = lock
      self.state.door_rl = lock
      self.state.door_rr = lock
      self._broadcast()
    elif frame.arbitration_id == MsgId.STEER_CMD:
      # Simulated steer torque nudges speed slightly (for demo feedback)
      if self.state.ignition and frame.data:
        steer = int.from_bytes(frame.data[:2], "little", signed=True)
        self.state.speed_kph = max(0.0, min(120.0, self.state.speed_kph + steer * 0.01))
    elif frame.arbitration_id == MsgId.GAS_CMD and self.state.ignition and frame.data:
      throttle = frame.data[0] / 255.0
      self.state.speed_kph = min(120.0, self.state.speed_kph + throttle * 2.0)
    elif frame.arbitration_id == MsgId.BRAKE_CMD and frame.data:
      brake = frame.data[0] / 255.0
      self.state.speed_kph = max(0.0, self.state.speed_kph - brake * 5.0)

  def set_ignition(self, on: bool) -> None:
    self.state.ignition = on
    if on and self.state.rpm < 400:
      self.state.rpm = 800
    self._broadcast()

  def snapshot(self) -> dict:
    return {
      "speed_kph": round(self.state.speed_kph, 1),
      "rpm": self.state.rpm,
      "ignition": self.state.ignition,
      "doors": unpack_door_status(pack_door_status(
        self.state.door_fl, self.state.door_fr,
        self.state.door_rl, self.state.door_rr, self.state.trunk,
      )),
      "ecus": dict(self.state.ecus),
    }
