"""Virtual ESP32 security gateway: auth, CAN firewall, request forwarding."""

from __future__ import annotations

import secrets
from dataclasses import dataclass
from enum import Enum

from Crypto.PublicKey import ECC

from opendbc.simulation.auth import AuthEngine, KeyPair, SessionToken
from opendbc.simulation.can_bus import CANBus, CANFrame
from opendbc.simulation.protocol import DANGEROUS_IDS, READ_ONLY_IDS, SAFE_WRITE_IDS


class GatewayDecision(str, Enum):
  ALLOW = "allow"
  BLOCK_NO_AUTH = "block_no_auth"
  BLOCK_DANGEROUS = "block_dangerous"
  BLOCK_REPLAY = "block_replay"
  BLOCK_UNKNOWN_ID = "block_unknown_id"


@dataclass(frozen=True)
class GatewayResult:
  decision: GatewayDecision
  message: str
  frame: CANFrame | None = None


class SecurityGateway:
  """
  Acts as virtual ESP32 between clients and the vehicle CAN bus.

  Mirrors opendbc safety: actuation (steer/brake/gas) requires auth + controls_allowed.
  """

  def __init__(
    self,
    bus: CANBus,
    auth: AuthEngine,
    trusted_public_key: ECC.EccKey,
  ) -> None:
    self.bus = bus
    self.auth = auth
    self.trusted_public_key = trusted_public_key
    self.controls_allowed = False
    self._session: SessionToken | None = None
    self._audit: list[GatewayResult] = []

  def authenticate_client(self, client_keys: KeyPair) -> tuple[SessionToken | None, str]:
    """Challenge-response: client signs nonce, gateway verifies."""
    ch = self.auth.issue_challenge()
    signature = client_keys.sign(ch.nonce)
    session = self.auth.verify_challenge_response(
      ch.challenge_id,
      signature,
      client_keys.public_key,
      subject="authorized_client",
    )
    if session is None:
      return None, "signature verification failed"
    if client_keys.public_key.export_key(format="DER") != self.trusted_public_key.export_key(format="DER"):
      return None, "public key not trusted"
    self._session = session
    return session, "access granted"

  @property
  def session(self) -> SessionToken | None:
    return self._session

  def logout(self) -> None:
    self._session = None
    self.controls_allowed = False

  def enable_controls(self) -> None:
    """Like openpilot heartbeat + safety mode allowing actuation."""
    if self._session is not None:
      self.controls_allowed = True

  def send_can(
    self,
    frame: CANFrame,
    session_token: str | None = None,
    request_id: str | None = None,
  ) -> GatewayResult:
    token = session_token or (self._session.token if self._session else None)
    session = self.auth.validate_session(token) if token else None

    if request_id is not None and not self.auth.register_request_id(request_id):
      result = GatewayResult(
        GatewayDecision.BLOCK_REPLAY,
        f"replay detected: request_id={request_id}",
      )
      self._audit.append(result)
      return result

    msg_id = frame.arbitration_id

    if msg_id in READ_ONLY_IDS:
      result = GatewayResult(GatewayDecision.ALLOW, "telemetry pass-through", frame)
      self._audit.append(result)
      return result

    if session is None:
      result = GatewayResult(GatewayDecision.BLOCK_NO_AUTH, f"no valid session for 0x{msg_id:03X}")
      self._audit.append(result)
      return result

    if msg_id in DANGEROUS_IDS:
      if not self.controls_allowed:
        result = GatewayResult(
          GatewayDecision.BLOCK_DANGEROUS,
          f"actuation blocked (controls_allowed=False) for 0x{msg_id:03X}",
        )
        self._audit.append(result)
        return result

    if msg_id in SAFE_WRITE_IDS or msg_id in DANGEROUS_IDS:
      self.bus.send(frame)
      result = GatewayResult(GatewayDecision.ALLOW, f"forwarded 0x{msg_id:03X} to vehicle bus", frame)
      self._audit.append(result)
      return result

    result = GatewayResult(GatewayDecision.BLOCK_UNKNOWN_ID, f"unknown CAN ID 0x{msg_id:03X}")
    self._audit.append(result)
    return result

  def audit_log(self) -> list[GatewayResult]:
    return list(self._audit)

  @staticmethod
  def new_request_id() -> str:
    return secrets.token_hex(8)
