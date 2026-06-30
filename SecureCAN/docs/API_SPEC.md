# API Specification — SecureCAN Gateway Protocol

## Purpose

Define the binary protocol used for communication between the SecureCAN mobile app and the SecureCAN Gateway over BLE and Wi-Fi.

## Scope

This document specifies all message types, frame formats, command codes, and data serialisation. Both BLE GATT characteristic format and Wi-Fi TCP packet format are covered.

## Transport Overview

| Transport | Interface | Max Payload | Encryption |
|-----------|-----------|-------------|------------|
| BLE 5.0 | GATT Characteristic (Notify + Write) | 512 bytes per packet | LE Secure Connections |
| Wi-Fi | TCP port 8670 | 1460 bytes per packet | Optional TLS |

## BLE GATT Service

| Service UUID | Description |
|-------------|-------------|
| `F000C000-0451-4000-B000-000000000000` | SecureCAN Gateway Service |

### Characteristics

| Characteristic | UUID | Properties | Description |
|---------------|------|------------|-------------|
| Command TX | `F000C001-0451-4000-B000-000000000000` | Write | App → Gateway commands |
| Response RX | `F000C002-0451-4000-B000-000000000000` | Notify | Gateway → App responses |
| Frame Stream | `F000C003-0451-4000-B000-000000000000` | Notify | Raw CAN frame stream |
| Auth Challenge | `F000C004-0451-4000-B000-000000000000` | Write+Notify | Authentication handshake |

## Binary Packet Format

All packets use a 4-byte header followed by a variable-length payload.

```
┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
│Byte 0│Byte 1│Byte 2│Byte 3│Byte 4...n-1│Byte n│
├─────┼─────┼─────┼─────┼───────────────┼──────┤
│Magic│Flags│Sequence│ Message Type │ Payload │ CRC8 │
│0x5C │ 0x01│ (2B)  │    (1B)      │  (var)  │ (1B) │
└─────┴─────┴─────┴─────┴───────────────┴──────┘
```

### Header Fields

| Field | Size | Description |
|-------|------|-------------|
| Magic | 1 byte | Always 0x5C ('\\') |
| Flags | 1 byte | Bit 0: Encrypted, Bit 1: Compressed, Bit 2: Ack Requested |
| Sequence | 2 bytes | Big-endian, wraps at 65535 |
| Message Type | 1 byte | See message types below |
| Payload | Variable | Message-specific data |
| CRC8 | 1 byte | CRC-8-ATM over header + payload |

## Message Types

| Code | Name | Direction | Description |
|------|------|-----------|-------------|
| 0x01 | PING | Bidirectional | Keep-alive |
| 0x02 | PONG | Bidirectional | Keep-alive response |
| 0x10 | AUTH_CHALLENGE_REQ | App → Gateway | Request authentication challenge |
| 0x11 | AUTH_CHALLENGE | Gateway → App | Challenge nonce (32 bytes) |
| 0x12 | AUTH_APP_SIGN | App → Gateway | App-signed nonce (signature 64 bytes) |
| 0x13 | AUTH_GW_RESPONSE | Gateway → App | Gateway-signed nonce + gateway nonce |
| 0x14 | AUTH_VERIFY | App → Gateway | Send verification result |
| 0x15 | AUTH_STATUS | Gateway → App | Authentication state |
| 0x20 | CAN_FRAME | Gateway → App | Single raw CAN frame |
| 0x21 | CAN_BATCH | Gateway → App | Batch of CAN frames |
| 0x22 | CAN_STATS | Gateway → App | CAN bus statistics |
| 0x30 | CONFIG_GET | App → Gateway | Request configuration value |
| 0x31 | CONFIG_SET | App → Gateway | Set configuration value |
| 0x32 | CONFIG_VALUE | Gateway → App | Configuration value response |
| 0x40 | FW_VERSION | Bidirectional | Firmware version query/response |
| 0x41 | FW_UPDATE | App → Gateway | Firmware update chunk |
| 0x42 | FW_UPDATE_STATUS | Gateway → App | Update progress/status |
| 0x50 | GATEWAY_STATUS | Gateway → App | Health status |
| 0x51 | GATEWAY_RESET | App → Gateway | Soft reset command |
| 0x60 | ERROR | Gateway → App | Error notification |

## CAN Frame Format (Message Type 0x20)

```
┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬──────────────┐
│Timestamp(4B)│ CAN ID(4B) │Flags │ DLC  │ Data (0-8 bytes) │
│  (ms)      │            │ (1B) │ (1B) │                   │
└─────┴─────┴─────┴─────┴─────┴─────┴─────┴──────────────┘
```

| Field | Size | Description |
|-------|------|-------------|
| Timestamp | 4 bytes | Milliseconds since gateway boot |
| CAN ID | 4 bytes | 11-bit or 29-bit ID, big-endian |
| Flags | 1 byte | Bit 0: Extended frame (29-bit), Bit 1: Remote frame |
| DLC | 1 byte | Data length code (0-8) |
| Data | 0-8 bytes | CAN frame data payload |

## Authentication Handshake

### Sequence (Mutual Authentication)

```
App                                Gateway
 │                                     │
 │── AUTH_CHALLENGE_REQ ─────────────>│
 │                                     │
 │<── AUTH_CHALLENGE(nonce_G 32B) ────│  (gateway generates nonce_G)
 │                                     │
 │── AUTH_APP_SIGN(sig_G 64B) ───────>│  (sign(nonce_G, user_private_key))
 │                                     │  (gateway verifies sig_G with user_public_key)
 │                                     │  (gateway generates nonce_A)
 │<── AUTH_GW_RESPONSE(nonce_A +      │  (sign(nonce_G || nonce_A, gateway_private_key))
 │        sig_A 64B) ─────────────────│
 │                                     │  (app verifies sig_A with gateway_public_key)
 │── AUTH_VERIFY(result 1B) ─────────>│  (0=success, 1=failure)
 │                                     │
 │<── AUTH_STATUS(state 1B) ───────────│  (0=unauthenticated, 1=authenticated)
```

### Mutual Authentication Flow

1. **Key Exchange (out-of-band, one-time)**
   - User generates Ed25519 keypair on mobile device
   - Gateway generates Ed25519 keypair on first boot
   - App public key transferred to gateway via QR code or manual entry
   - Gateway public key transferred to app via QR code
   - Both parties store the other's public key

2. **Challenge (per-session)**
   - App sends AUTH_CHALLENGE_REQ to gateway
   - Gateway generates random 32-byte nonce (nonce_G), sends it to app
   - App signs nonce_G with user's private key, sends AUTH_APP_SIGN
   - Gateway verifies signature using stored user public key
     - On failure: abort, send AUTH_STATUS(unauthenticated)

3. **Response (per-session)**
   - Gateway generates second random 32-byte nonce (nonce_A)
   - Gateway signs concatenation (nonce_G || nonce_A) with gateway's private key
   - Gateway sends AUTH_GW_RESPONSE containing nonce_A + signature
   - App verifies signature using stored gateway public key
     - On failure: send AUTH_VERIFY(failure)

4. **Verification**
   - App sends AUTH_VERIFY(result) — 0 = both sides authenticated, 1 = failure
   - Gateway responds with AUTH_STATUS(state) — 0 = unauthenticated, 1 = authenticated
   - Both parties must have successfully verified the other for authentication to succeed

## Error Codes

| Code | Description |
|------|-------------|
| 0x01 | Unknown message type |
| 0x02 | Invalid CRC |
| 0x03 | Authentication required |
| 0x04 | Invalid sequence number |
| 0x05 | Payload too large |
| 0x06 | Configuration key not found |
| 0x07 | Configuration value invalid |
| 0x08 | Firmware update in progress |
| 0x09 | Hardware write-enable disabled |
| 0x10 | Internal error |

## Wi-Fi Protocol

When using Wi-Fi transport, the same binary packet format is used over a TCP stream. The gateway listens on port 8670. Clients connect and exchange packets bidirectionally. Each packet is prefixed with a 2-byte length field (big-endian) for stream framing:

```
┌──────────────┬─────────────────────────┐
│ Payload Len  │  Packet (binary format)  │
│ (2 bytes)    │  (variable)             │
└──────────────┴─────────────────────────┘
```

## Rate Limiting

- Gateway shall not exceed 100 packets per second to the app
- Authentication attempts limited to 3 per 30-second window
- CONFIG_SET limited to 10 per minute

---

**TODOs**

- [ ] Implement protocol dissector in Wireshark for debugging
- [ ] Add compression support for CAN_BATCH messages
- [ ] Define alert notification message type (0x23)
- [ ] Specify optional TLS certificate format for Wi-Fi transport
