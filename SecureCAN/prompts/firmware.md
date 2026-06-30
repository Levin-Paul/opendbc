# SecureCAN Firmware Development Prompt

## Context

You are building firmware for the SecureCAN Gateway — an ESP32-S3 based device that connects to the vehicle OBD-II port, captures CAN traffic, and streams it to the mobile app over BLE.

## Architecture

- **Platform**: ESP32-S3 (Xtensa LX7 dual-core, 240 MHz)
- **Framework**: ESP-IDF v5.x
- **Language**: C
- **CAN Controller**: TWAI (built-in)
- **CAN Transceiver**: SN65HVD230
- **Wireless**: BLE 5.0 (primary), Wi-Fi (secondary)
- **Authentication**: Ed25519 challenge-response

## Key Files to Reference

- `docs/HARDWARE_ARCHITECTURE.md` — Hardware design and pinouts
- `docs/API_SPEC.md` — BLE protocol specification (binary format)
- `docs/SECURITY_MODEL.md` — Secure boot, firmware signing, key management
- `docs/TRUST_MODEL.md` — Trust boundaries and assumptions

## Firmware Structure

```
firmware/esp32/
├── main/
│   ├── app_main.c           # Entry point, init sequence
│   ├── can/
│   │   ├── can_controller.c # TWAI init, frame RX/TX
│   │   └── can_buffer.c     # Ring buffer for frames
│   ├── ble/
│   │   ├── ble_gatt.c       # GATT service and characteristics
│   │   └── ble_adv.c        # Advertising configuration
│   ├── auth/
│   │   ├── ed25519.c        # Ed25519 sign/verify
│   │   └── session.c        # Session management
│   ├── proto/
│   │   ├── protocol.c       # Binary protocol encode/decode
│   │   └── crc8.c           # CRC8-ATM calculation
│   ├── config/
│   │   └── nvs_config.c     # NVS read/write
│   ├── update/
│   │   └── ota_update.c     # OTA firmware update
│   └── util/
│       ├── watchdog.c       # Watchdog timer
│       └── led.c            # Status LED control
├── test/                     # Unity test framework
└── CMakeLists.txt
```

## Key Components

### CAN Controller

- Initialize TWAI at 500 kbps (default)
- Listen-only mode for MVP (hardware-enforced)
- Ring buffer holds 1000+ frames during BLE transmission gaps
- Timestamp each frame with microsecond precision

### BLE GATT Service

- Service UUID: F000C000-0451-4000-B000-000000000000
- Characteristics: Command TX, Response RX, Frame Stream, Auth Challenge
- MTU negotiation up to 512 bytes
- Connection parameters optimised for throughput

### Authentication Engine

- Generate Ed25519 keypair on first boot
- Store private key in encrypted NVS
- Expose public key via QR code
- Sign challenge nonces during handshake
- Reject config changes when unauthenticated

## Safety Critical Rules

1. **TWAI write enable is controlled by hardware DIP switch** — firmware must read GPIO state and refuse to initialise TWAI transmitter if switch is disabled
2. **Watchdog timer must be serviced in main loop** — 30 second timeout, resets device if thread hangs
3. **OTA update must verify signature before applying** — reject unsigned firmware
4. **CAN frames must never be stored persistently on gateway** — RAM buffer only
5. **All BLE characteristics must require encryption** — no unprotected access

## Testing

- Unit tests with ESP-IDF Unity test framework: `idf.py test`
- CAN loopback testing on bench
- BLE throughput benchmarks
- Power consumption measurement

---

**TODOs**

- [ ] Implement TWAI controller with listen-only mode
- [ ] Build BLE GATT service with binary protocol
- [ ] Write Ed25519 authentication module
- [ ] Implement ring buffer with overflow protection
- [ ] Create OTA update mechanism with signature verification
