# Security Model — SecureCAN

## Purpose

Define the complete security model governing SecureCAN's authentication, authorisation, encryption, key management, and secure boot architecture.

## Scope

This document covers all security controls implemented in the SecureCAN Gateway firmware and mobile application. It spans cryptographic protocols, key lifecycle, secure storage, and communication security.

## Authentication Architecture

```
┌─────────────────────────────────────────────────────────────┐
│               Mutual Authentication Flow                      │
│                                                              │
│  Mobile App                        Gateway                   │
│  ┌──────────────┐                 ┌──────────────┐          │
│  │ Ed25519      │                 │ Ed25519      │          │
│  │ Keypair (user)│                 │ Keypair (device)│       │
│  │              │                 │              │          │
│  │ Public Key A │───out-of-band──→│ Store Pub A  │          │
│  │              │                 │              │          │
│  │              │◄───QR code──────│ Public Key B │          │
│  │ Store Pub B  │                 │              │          │
│  └──────┬───────┘                 └──────┬───────┘          │
│         │                                │                   │
│         │──AUTH_CHALLENGE_REQ────────────│                   │
│         │                                │                   │
│         │◄──AUTH_CHALLENGE(nonce_G)──────│  (gateway challenges app)
│         │                                │                   │
│         │──AUTH_APP_SIGN(sig_G)─────────>│  (app signs nonce_G)
│         │                                │  (gateway verifies app)
│         │                                │                   │
│         │◄──AUTH_GW_RESPONSE(nonce_A +  │  (gateway signs nonce_G||nonce_A)
│         │        sig_A)─────────────────│                   │
│         │  (app verifies gateway)       │                   │
│         │                                │                   │
│         │──AUTH_VERIFY(result)───────────│                   │
│         │                                │                   │
│         │◄──AUTH_STATUS(authenticated)───│                   │
└─────────────────────────────────────────────────────────────┘
```

## Cryptographic Specifications

| Parameter | Specification |
|-----------|--------------|
| Signature Algorithm | Ed25519 (RFC 8032) |
| Key Size | 256-bit |
| Hash Function | SHA-256 |
| BLE Encryption | LE Secure Connections (AES-CCM) |
| Firmware Signature | Ed25519 |
| Random Nonce | 32 bytes from CSPRNG |
| Session Key Derivation | HKDF-SHA256 |

## Key Lifecycle

### Generation

- **User Keypair**: Generated on mobile device using platform CSPRNG (SecRandomCopyBytes on iOS, SecureRandom on Android)
- **Gateway Keypair**: Generated on ESP32 at first boot using hardware RNG, stored in NVS (Non-Volatile Storage) with encryption
- **Session Keys**: Derived per-connection using HKDF with the authentication nonce and both public keys as input

### Storage

| Key | Storage Location | Protection |
|-----|-----------------|------------|
| User Private Key | iOS Keychain / Android Keystore | Hardware-backed encryption |
| User Public Key | SQLite database | Integrity-only |
| Gateway Private Key | ESP32 NVS (encrypted) | Flash encryption |
| Gateway Public Key | SQLite database | Integrity-only |
| Gateway Public Key (on app) | SQLite database | Integrity-only |
| Session Key | In-memory only | Volatile |

### Rotation

- User keys rotated via Settings → Security → Rotate Keys
- Old keys are invalidated immediately
- Gateway re-pairing required after key rotation
- Gateway keys rotated on factory reset
- Session keys rotated on every new connection

### Revocation

- Compromised keys are revoked by deleting the corresponding public key from the paired device
- Factory reset on gateway clears all stored public keys
- User can unpair all gateways from Settings → Security → Manage Gateways

## Secure Boot and Firmware Updates

### Boot Chain

```
Boot ROM
  │
  ├── Verify bootloader signature ──→ Fail → Halt
  │
  ▼
Bootloader
  │
  ├── Verify partition table signature ──→ Fail → Halt
  │
  ▼
Partition Table
  │
  ├── Verify factory app signature ──→ Fail → Fallback to recovery
  │
  ▼
Application
  │
  ├── Verify OTA app signature (if present) ──→ Fail → Fallback to factory
  │
  ▼
Running Application
```

### Firmware Update Process

1. App downloads signed firmware binary from user-provided source (no auto-checkin)
2. App transfers binary to gateway in chunks via BLE (MSG_FW_UPDATE)
3. Gateway writes chunks to OTA partition
4. Gateway verifies Ed25519 signature on complete binary
5. On success: Gateway sets boot partition to OTA and reboots
6. On failure: Gateway erases OTA partition, boots factory app

## Communication Security

### BLE Security

- BLE 5.0 LE Secure Connections mandatory
- MITM protection enabled (passkey entry during pairing)
- No legacy pairing fallback
- All GATT characteristics require encryption

### Wi-Fi Security (Optional)

- TLS 1.3 for TCP transport
- Client certificate authentication optional (Phase 2)
- mDNS discovery with authenticated responses

## Threat Mitigation Summary

| Threat | Control |
|--------|---------|
| Gateway impersonation | Mutual Ed25519 challenge-response (app verifies gateway) |
| App impersonation | Mutual Ed25519 challenge-response (gateway verifies app) |
| BLE eavesdropping | LE Secure Connections encryption |
| BLE MITM | Passkey entry during pairing |
| Firmware tampering | Signed images, verified boot |
| Physical gateway tampering | Secure enclave (MVP: basic), hardware write-disable |
| Database theft | Platform key storage for secrets |
| Replay attacks | Unique nonce per authentication attempt |

## Penetration Testing Considerations

- BLE stack: BlueZ, btlejack for passive sniffing
- CAN interface: SocketCAN virtual interface for injection testing
- Firmware: ESP32 flash encryption bypass techniques
- Mobile app: Frida, Objection for runtime analysis

---

**TODOs**

- [ ] Complete cryptographic review by third-party auditor
- [ ] Implement key attestation for iOS Secure Enclave and Android TEE
- [ ] Define incident response for key compromise
- [ ] Add hardware security module (HSM) to gateway in Phase 4
