# Project Context — SecureCAN

## Origin

SecureCAN was initiated to address the gap between sophisticated vehicle cybersecurity research and practical tools available to vehicle owners. The OpenDBC project (comma.ai) provided the CAN decoding foundation. The ESP32 platform provided the affordable, accessible hardware gateway. The combination enables a class of vehicle security tools previously limited to research labs and OEM tooling.

## Technical Context

| Aspect | Detail |
|--------|--------|
| CAN Decoder | OpenDBC (external submodule, read-only) |
| Gateway MCU | ESP32-S3 with BLE 5.0 and Wi-Fi |
| Mobile App | React Native (iOS + Android) |
| Authentication | Ed25519 challenge-response |
| Storage | SQLite via React Native (local only) |
| Firmware Lang | C (ESP-IDF v5.x) |
| Attack Library | JSON-defined attack signatures |
| Integrity Model | SHA-256 fingerprints with baseline snapshots |
| Maintenance Engine | Signal trend analysis with configurable thresholds |

## Repository Architecture

```
SecureCAN/               # Main project (this repository)
  ├── opendbc/           # Git submodule — commaai/opendbc (read-only)
  ├── src/               # React Native application source
  ├── firmware/          # ESP32 gateway firmware source
  ├── docs/              # Project documentation
  ├── configs/           # Configuration and rule definitions
  ├── prompts/           # AI development prompt library
  └── memory/            # Sprint and decision tracking
```

## OpenDBC Boundary

The `opendbc/` directory is a git submodule pinned to a specific upstream commit. SecureCAN code must never:

- Modify any file inside `opendbc/`
- Add custom DBC definitions to `opendbc/`
- Rely on unmerged OpenDBC pull requests
- Copy OpenDBC source into SecureCAN source trees

Instead, SecureCAN builds a **Decoder Adapter Layer** that wraps OpenDBC parsers and normalizes signal output into SecureCAN's internal signal model. Vehicle-specific adapters inherit from a base decoder interface.

## Current Phase

**Pre-alpha / MVP Development**

The immediate goal is a read-only MVP that demonstrates:

1. ESP32 gateway successfully capturing CAN traffic
2. BLE/Wi-Fi streaming of raw CAN frames to mobile app
3. OpenDBC decoding of at least 3 vehicle profiles
4. Real-time dashboard displaying decoded signals
5. Basic threat detection against known attack patterns
6. ECU fingerprinting and integrity snapshot
7. Predictive maintenance alerts for battery and DPF

## Known Constraints

- OpenDBC does not cover all vehicles; coverage is limited to makes/models supported by comma.ai's openpilot
- ESP32 dual-core architecture limits CAN bit rate processing to 500 kbps without frame loss
- BLE throughput caps at approximately 80 Kbps, suitable for authentication, alerts, health data, and low-rate telemetry only; bulk CAN frame capture requires Wi-Fi transport
- React Native BLE libraries have platform-specific fragmentation on Android

---

**TODOs**

- [ ] Document all OpenDBC vehicle coverage gaps
- [ ] Benchmark ESP32 CAN frame capture throughput
- [ ] Evaluate BLE 5.0 Coded PHY for extended range
- [ ] Benchmark Wi-Fi TCP throughput for bulk CAN frame transfer
- [ ] Identify and document all React Native BLE library compatibility issues
