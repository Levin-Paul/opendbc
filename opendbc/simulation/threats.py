"""Simulated attacks: unauthorized access, replay, CAN injection."""

from __future__ import annotations

from opendbc.simulation.auth import KeyPair
from opendbc.simulation.can_bus import CANFrame
from opendbc.simulation.gateway import GatewayDecision, SecurityGateway
from opendbc.simulation.protocol import MsgId


class ThreatSimulator:
  def __init__(self, gateway: SecurityGateway, attacker_keys: KeyPair | None = None) -> None:
    self.gateway = gateway
    self.attacker_keys = attacker_keys or KeyPair.generate()

  def unauthorized_access(self) -> dict:
    """Send actuation without logging in."""
    self.gateway.logout()
    frame = CANFrame(MsgId.STEER_CMD, b"\x10\x00")
    result = self.gateway.send_can(frame, session_token=None, request_id=SecurityGateway.new_request_id())
    return {
      "attack": "unauthorized_access",
      "expected": GatewayDecision.BLOCK_NO_AUTH.value,
      "got": result.decision.value,
      "detail": result.message,
      "blocked": result.decision != GatewayDecision.ALLOW,
    }

  def replay_attack(self, captured_request_id: str, session_token: str) -> dict:
    """Reuse a prior request_id with a valid session."""
    frame = CANFrame(MsgId.DOOR_CMD, b"\x01")
    first = self.gateway.send_can(frame, session_token=session_token, request_id=captured_request_id)
    second = self.gateway.send_can(frame, session_token=session_token, request_id=captured_request_id)
    return {
      "attack": "replay",
      "expected": GatewayDecision.BLOCK_REPLAY.value,
      "first": first.decision.value,
      "second": second.decision.value,
      "detail": second.message,
      "blocked": second.decision == GatewayDecision.BLOCK_REPLAY,
    }

  def can_injection(self) -> dict:
    """Inject arbitrary / dangerous frame with stolen or no credentials."""
    self.gateway.logout()
    # Unknown ID
    unknown = self.gateway.send_can(
      CANFrame(0x7FF, b"\xDE\xAD\xBE\xEF"),
      session_token="forged.token",
      request_id=SecurityGateway.new_request_id(),
    )
    # Dangerous actuation with fake session
    steer = self.gateway.send_can(
      CANFrame(MsgId.GAS_CMD, b"\xFF"),
      session_token="dead.beef",
      request_id=SecurityGateway.new_request_id(),
    )
    return {
      "attack": "can_injection",
      "unknown_id_blocked": unknown.decision != GatewayDecision.ALLOW,
      "unknown_detail": unknown.message,
      "actuation_blocked": steer.decision != GatewayDecision.ALLOW,
      "actuation_detail": steer.message,
    }

  def wrong_key_auth(self) -> dict:
    """Attacker signs challenge with their own key (not in gateway trust store)."""
    session, msg = self.gateway.authenticate_client(self.attacker_keys)
    return {
      "attack": "wrong_key",
      "session_issued": session is not None,
      "blocked": session is None,
      "detail": msg,
    }
