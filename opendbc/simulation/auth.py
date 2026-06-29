"""Challenge-response authentication with ECDSA and session tokens."""

from __future__ import annotations

import hashlib
import hmac
import secrets
import time
from dataclasses import dataclass

from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS


@dataclass(frozen=True)
class KeyPair:
  private_key: ECC.EccKey
  public_key: ECC.EccKey

  @classmethod
  def generate(cls) -> KeyPair:
    private_key = ECC.generate(curve="P-256")
    return cls(private_key=private_key, public_key=private_key.public_key())

  def sign(self, message: bytes) -> bytes:
    signer = DSS.new(self.private_key, "fips-186-3", encoding="der")
    h = SHA256.new(message)
    return signer.sign(h)

  def verify(self, message: bytes, signature: bytes) -> bool:
    return verify_signature(self.public_key, message, signature)


def verify_signature(public_key: ECC.EccKey, message: bytes, signature: bytes) -> bool:
  verifier = DSS.new(public_key, "fips-186-3", encoding="der")
  h = SHA256.new(message)
  try:
    verifier.verify(h, signature)
  except (ValueError, TypeError):
    return False
  else:
    return True


@dataclass(frozen=True)
class SessionToken:
  token: str
  expires_at: float
  subject: str


@dataclass
class Challenge:
  nonce: bytes
  challenge_id: str
  expires_at: float


class AuthEngine:
  """Virtual ESP32 auth: nonce challenge, ECDSA verify, HMAC session token."""

  def __init__(self, server_secret: bytes | None = None, session_ttl_s: float = 300.0) -> None:
    self._server_secret = server_secret or secrets.token_bytes(32)
    self._session_ttl_s = session_ttl_s
    self._challenges: dict[str, Challenge] = {}
    self._used_challenges: set[str] = set()
    self._sessions: dict[str, SessionToken] = {}
    self._used_request_ids: dict[str, float] = {}  # replay protection

  def issue_challenge(self) -> Challenge:
    challenge_id = secrets.token_hex(8)
    nonce = secrets.token_bytes(32)
    ch = Challenge(
      nonce=nonce,
      challenge_id=challenge_id,
      expires_at=time.time() + 30.0,
    )
    self._challenges[challenge_id] = ch
    return ch

  def verify_challenge_response(
    self,
    challenge_id: str,
    signature: bytes,
    public_key: ECC.EccKey,
    subject: str = "demo_client",
  ) -> SessionToken | None:
    ch = self._challenges.pop(challenge_id, None)
    if ch is None or ch.challenge_id in self._used_challenges:
      return None
    if time.time() > ch.expires_at:
      return None

    if not verify_signature(public_key, ch.nonce, signature):
      return None

    self._used_challenges.add(challenge_id)
    return self._mint_session(subject)

  def _mint_session(self, subject: str) -> SessionToken:
    session_id = secrets.token_hex(16)
    expires_at = time.time() + self._session_ttl_s
    payload = f"{session_id}|{subject}|{expires_at:.3f}".encode()
    mac = hmac.new(self._server_secret, payload, hashlib.sha256).hexdigest()
    token = f"{session_id}.{mac}"
    session = SessionToken(token=token, expires_at=expires_at, subject=subject)
    self._sessions[session_id] = session
    return session

  def validate_session(self, token: str) -> SessionToken | None:
    parts = token.split(".", 1)
    if len(parts) != 2:
      return None
    session_id, mac = parts
    session = self._sessions.get(session_id)
    if session is None or session.token != token:
      return None
    if time.time() > session.expires_at:
      self._sessions.pop(session_id, None)
      return None
    payload = f"{session_id}|{session.subject}|{session.expires_at:.3f}".encode()
    expected = hmac.new(self._server_secret, payload, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(mac, expected):
      return None
    return session

  def register_request_id(self, request_id: str, ttl_s: float = 60.0) -> bool:
    """Return False if request_id was already seen (replay)."""
    now = time.time()
    self._purge_request_ids(now)
    if request_id in self._used_request_ids:
      return False
    self._used_request_ids[request_id] = now + ttl_s
    return True

  def _purge_request_ids(self, now: float) -> None:
    expired = [rid for rid, exp in self._used_request_ids.items() if exp < now]
    for rid in expired:
      del self._used_request_ids[rid]
