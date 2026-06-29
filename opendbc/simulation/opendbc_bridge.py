"""Pack/decode CAN using real OpenDBC definitions."""

from __future__ import annotations

import math
import time
from typing import Any

from opendbc.can.dbc import DBC, Signal

from opendbc.simulation.profiles import SignalRef, VehicleProfile


class OpenDBCBridge:
  def __init__(self, profile: VehicleProfile) -> None:
    self.profile = profile
    self._dbc: DBC | None = None
    try:
      self._dbc = DBC(profile.dbc)
    except Exception:
      self._dbc = None

  @property
  def available(self) -> bool:
    return self._dbc is not None

  def _addr(self, ref: SignalRef) -> int | None:
    if self._dbc is None:
      return None
    msg = self._dbc.name_to_msg.get(ref.message)
    return msg.address if msg else None

  def pack_signal(self, ref: SignalRef, value: float) -> tuple[int, bytes] | None:
    if self._dbc is None:
      return None
    addr = self._addr(ref)
    if addr is None:
      return None
    try:
      msg = self._dbc.addr_to_msg.get(addr)
      if msg is None:
        return None
      data = bytearray(msg.size)
      sig = msg.sigs.get(ref.signal)
      if sig is None:
        return None
      ival = int(math.floor((value - sig.offset) / sig.factor + 0.5))
      if ival < 0:
        ival = (1 << sig.size) + ival
      self._set_value(data, sig, ival)
      return addr, bytes(data)
    except Exception:
      return None

  @staticmethod
  def _set_value(msg: bytearray, sig: Signal, ival: int) -> None:
    i = sig.lsb // 8
    bits = sig.size
    while bits > 0:
      lsb = sig.lsb if (sig.lsb // 8) == i else i * 8
      msb = sig.msb if (sig.msb // 8) == i else (i + 1) * 8 - 1
      size = msb - lsb + 1
      d = (ival >> (bits - size)) & ((1 << size) - 1)
      msg[i] |= d << (lsb - (i * 8))
      bits -= size
      i = i - 1 if sig.is_little_endian else i + 1

  def decode_frame(self, address: int, data: bytes) -> list[dict[str, Any]]:
    if self._dbc is None:
      return []
    msg = self._dbc.addr_to_msg.get(address)
    if msg is None:
      return []
    decoded: list[dict[str, Any]] = []
    for name, sig in msg.sigs.items():
      try:
        from opendbc.can.parser import get_raw_value
        raw = get_raw_value(data, sig)
        if sig.is_signed:
          raw -= ((raw >> (sig.size - 1)) & 0x1) * (1 << sig.size)
        val = raw * sig.factor + sig.offset
        decoded.append({"signal": name, "value": round(val, 2), "unit": sig.unit or ""})
      except Exception:
        continue
    return decoded

  def build_telemetry_frames(self, state: dict) -> list[dict]:
    """Emit realistic CAN frames for inspector."""
    frames: list[dict] = []
    ts = time.time()
    pairs = [
      (self.profile.speed, state.get("speed_kph", 0.0)),
    ]
    if self.profile.rpm and state.get("rpm") is not None:
      pairs.append((self.profile.rpm, float(state["rpm"])))
    if self.profile.steer and state.get("steering_angle") is not None:
      pairs.append((self.profile.steer, float(state["steering_angle"])))
    if self.profile.brake is not None:
      pairs.append((self.profile.brake, 1.0 if state.get("brake_pressed") else 0.0))

    for ref, value in pairs:
      packed = self.pack_signal(ref, value)
      if packed is None:
        continue
      addr, data = packed
      frames.append({
        "timestamp": ts,
        "address": addr,
        "address_hex": f"0x{addr:X}",
        "data_hex": data.hex(" ").upper(),
        "message": ref.message,
        "primary_signal": ref.signal,
        "decoded": self.decode_frame(addr, data),
      })
    return frames
