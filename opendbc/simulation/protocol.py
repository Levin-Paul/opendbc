"""Demo CAN IDs and frame layout (mirrors opendbc safety: block actuation without auth)."""

from enum import IntEnum


class MsgId(IntEnum):
  VEHICLE_STATE = 0x100
  DOOR_STATUS = 0x101
  ECU_HEARTBEAT = 0x102
  STEER_CMD = 0x200
  BRAKE_CMD = 0x201
  GAS_CMD = 0x202
  DOOR_CMD = 0x210


# Actuation IDs blocked unless controls_allowed (see opendbc/safety/safety.h)
DANGEROUS_IDS = frozenset({MsgId.STEER_CMD, MsgId.BRAKE_CMD, MsgId.GAS_CMD})
SAFE_WRITE_IDS = frozenset({MsgId.DOOR_CMD})
READ_ONLY_IDS = frozenset({MsgId.VEHICLE_STATE, MsgId.DOOR_STATUS, MsgId.ECU_HEARTBEAT})


def pack_vehicle_state(speed_kph: float, rpm: int, ignition: bool) -> bytes:
  return bytes([
    int(speed_kph) & 0xFF,
    (int(speed_kph) >> 8) & 0xFF,
    rpm & 0xFF,
    (rpm >> 8) & 0xFF,
    1 if ignition else 0,
  ])


def unpack_vehicle_state(data: bytes) -> dict:
  if len(data) < 5:
    return {"speed_kph": 0.0, "rpm": 0, "ignition": False}
  speed = data[0] | (data[1] << 8)
  rpm = data[2] | (data[3] << 8)
  return {"speed_kph": float(speed), "rpm": rpm, "ignition": bool(data[4])}


def pack_door_status(fl: bool, fr: bool, rl: bool, rr: bool, trunk: bool) -> bytes:
  mask = (fl) | (fr << 1) | (rl << 2) | (rr << 3) | (trunk << 4)
  return bytes([mask])


def unpack_door_status(data: bytes) -> dict[str, bool]:
  mask = data[0] if data else 0
  return {
    "door_fl": bool(mask & 1),
    "door_fr": bool(mask & 2),
    "door_rl": bool(mask & 4),
    "door_rr": bool(mask & 8),
    "trunk": bool(mask & 16),
  }


def pack_ecu_heartbeat(present: dict[str, bool]) -> bytes:
  names = ("ecm", "tcm", "abs", "eps", "bcm")
  mask = sum(1 << i for i, n in enumerate(names) if present.get(n, False))
  return bytes([mask])


def unpack_ecu_heartbeat(data: bytes) -> dict[str, bool]:
  mask = data[0] if data else 0
  names = ("ecm", "tcm", "abs", "eps", "bcm")
  return {n: bool(mask & (1 << i)) for i, n in enumerate(names)}
