"""In-process fake CAN bus (no hardware)."""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass, field


@dataclass(frozen=True)
class CANFrame:
  arbitration_id: int
  data: bytes
  bus: int = 0
  timestamp: float = field(default_factory=time.time)


Listener = Callable[[CANFrame], None]


class CANBus:
  """Simple publish/subscribe CAN simulator."""

  def __init__(self) -> None:
    self._listeners: list[Listener] = []
    self._log: list[CANFrame] = []

  def subscribe(self, listener: Listener) -> None:
    self._listeners.append(listener)

  def send(self, frame: CANFrame) -> None:
    self._log.append(frame)
    for listener in list(self._listeners):
      listener(frame)

  def history(self) -> list[CANFrame]:
    return list(self._log)

  def clear_history(self) -> None:
    self._log.clear()
