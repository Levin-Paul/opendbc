# Software Requirements Specification — SecureCAN

**Version:** 0.1.0  
**Status:** Draft  
**Last Updated:** 2026-06-30

## Purpose

This document specifies the functional and non-functional requirements for the SecureCAN platform. It serves as the authoritative reference for development, testing, and acceptance.

## Scope

SecureCAN is an offline-first vehicle cybersecurity and predictive maintenance platform consisting of:

1. **SecureCAN Gateway** — ESP32-based hardware connected to the vehicle OBD-II port
2. **SecureCAN Mobile App** — React Native application providing the user interface
3. **Decoder Adapter Layer** — Software bridge between OpenDBC and SecureCAN internal signal model

## Functional Requirements

### FR-01 — CAN Frame Capture

| ID | Requirement |
|----|-------------|
| FR-01-01 | The gateway shall capture CAN frames from the vehicle OBD-II port at bus speeds up to 500 kbps |
| FR-01-02 | The gateway shall support CAN 2.0A (11-bit) and CAN 2.0B (29-bit) identifier formats |
| FR-01-03 | The gateway shall timestamp each captured frame with microsecond precision |
| FR-01-04 | The gateway shall buffer a minimum of 1000 frames during BLE transmission gaps |

### FR-02 — CAN Frame Streaming

| ID | Requirement |
|----|-------------|
| FR-02-01 | The gateway shall stream captured CAN frames to the mobile app over Wi-Fi (TCP) for bulk capture |
| FR-02-02 | The gateway shall transmit authentication, alerts, health data, and low-rate telemetry over BLE 5.0 |
| FR-02-03 | The gateway shall support both BLE and Wi-Fi transports simultaneously where available |
| FR-02-04 | The mobile app shall reassemble and order frames by timestamp |
| FR-02-05 | Frame loss rate shall not exceed 0.1% under normal operating conditions |

### FR-03 — CAN Decoding

| ID | Requirement |
|----|-------------|
| FR-03-01 | The Decoder Adapter Layer shall load OpenDBC definitions for the detected vehicle |
| FR-03-02 | The Decoder Adapter Layer shall decode raw CAN frames into human-readable signals |
| FR-03-03 | The system shall support automatic vehicle identification via VIN or CAN message pattern |
| FR-03-04 | Decoded signals shall be available for display within 50 ms of frame reception |

### FR-04 — Authentication

| ID | Requirement |
|----|-------------|
| FR-04-01 | The mobile app and gateway shall mutually authenticate using Ed25519 challenge-response (both parties verify the other) |
| FR-04-02 | Key generation shall occur on the mobile device and gateway independently; private keys never leave their respective devices |
| FR-04-03 | Authentication must complete within 2 seconds over BLE |
| FR-04-04 | Failed authentication shall not prevent CAN monitoring; only configuration changes are restricted |

### FR-05 — Threat Detection

| ID | Requirement |
|----|-------------|
| FR-05-01 | The threat detection engine shall analyse decoded signals in real time |
| FR-05-02 | Detection rules shall be user-configurable via JSON configuration files |
| FR-05-03 | The engine shall detect CAN message injection attacks |
| FR-05-04 | The engine shall detect CAN message replay attacks |
| FR-05-05 | The engine shall detect ECU spoofing attacks |
| FR-05-06 | The engine shall detect bus-off attacks |
| FR-05-07 | Detection latency shall not exceed 200 ms from frame reception |

### FR-06 — ECU Integrity Verification

| ID | Requirement |
|----|-------------|
| FR-06-01 | The system shall generate ECU fingerprints from CAN message patterns |
| FR-06-02 | The system shall store ECU baseline snapshots for comparison |
| FR-06-03 | The system shall alert when ECU fingerprints deviate from baseline |
| FR-06-04 | Users shall be able to update baselines after verified maintenance events |

### FR-07 — Sensor Verification

| ID | Requirement |
|----|-------------|
| FR-07-01 | The system shall validate sensor readings against plausible ranges |
| FR-07-02 | The system shall perform cross-signal plausibility checks |
| FR-07-03 | The system shall detect sensor drift and calibration anomalies |

### FR-08 — Predictive Maintenance

| ID | Requirement |
|----|-------------|
| FR-08-01 | The system shall track signal trends over user-defined time windows |
| FR-08-02 | The system shall generate maintenance alerts when trends exceed thresholds |
| FR-08-03 | The system shall support battery voltage degradation monitoring |
| FR-08-04 | The system shall support DPF pressure monitoring |
| FR-08-05 | Users shall be able to define custom maintenance rules |

### FR-09 — CAN Firewall

| ID | Requirement |
|----|-------------|
| FR-09-01 | The firewall shall apply allow/block/drop rules to CAN messages |
| FR-09-02 | Firewall rules shall be user-configurable by CAN ID, data pattern, and frequency |
| FR-09-03 | The firewall shall log all blocked messages with reason codes |
| FR-09-04 | The firewall shall operate in monitor-only mode for MVP |

### FR-10 — Data Storage

| ID | Requirement |
|----|-------------|
| FR-10-01 | All data shall be stored locally on the user's mobile device |
| FR-10-02 | The system shall use SQLite for structured data storage |
| FR-10-03 | Users shall be able to export data in CSV and JSON formats |
| FR-10-04 | Data retention periods shall be user-configurable |

### FR-11 — Notifications

| ID | Requirement |
|----|-------------|
| FR-11-01 | The system shall generate notifications for security alerts |
| FR-11-02 | The system shall generate notifications for maintenance alerts |
| FR-11-03 | Notifications shall include severity level (INFO, WARNING, CRITICAL, EMERGENCY) |
| FR-11-04 | Notifications shall include timestamp, affected component, and recommended action |

## Non-Functional Requirements

### NFR-01 — Performance

| ID | Requirement |
|----|-------------|
| NFR-01-01 | CAN frame capture to dashboard display latency ≤ 100 ms |
| NFR-01-02 | Mobile app cold start time ≤ 3 seconds |
| NFR-01-03 | Gateway boot time ≤ 5 seconds |
| NFR-01-04 | BLE connection establishment ≤ 1 second |
| NFR-01-05 | Authentication handshake ≤ 2 seconds |

> **Validation note:** Gateway boot time (NFR-01-03) target must be validated during hardware testing. ESP32-S3 secure boot chain verification, NVS initialisation, and BLE stack startup may impact this target.

### NFR-02 — Reliability

| ID | Requirement |
|----|-------------|
| NFR-02-01 | Gateway uptime ≥ 99.9% under normal vehicle operating conditions |
| NFR-02-02 | Mobile app crash rate ≤ 0.1% of sessions |
| NFR-02-03 | Data integrity verification on every database write |

### NFR-03 — Security

| ID | Requirement |
|----|-------------|
| NFR-03-01 | All BLE communication encrypted using BLE 5.0 LE Secure Connections |
| NFR-03-02 | Authentication keys must be Ed25519 with minimum 256-bit security |
| NFR-03-03 | Firmware updates must be signed and verified before installation |
| NFR-03-04 | No plaintext secrets in firmware binary |

### NFR-04 — Compatibility

| ID | Requirement |
|----|-------------|
| NFR-04-01 | Mobile app shall support iOS 15+ and Android 12+ |
| NFR-04-02 | Gateway shall support OBD-II pin assignments per SAE J1962 |
| NFR-04-03 | Gateway shall support CAN bit rates of 33.3, 50, 83.3, 100, 125, 250, and 500 kbps |

### NFR-05 — Usability

| ID | Requirement |
|----|-------------|
| NFR-05-01 | All alerts must include human-readable explanations |
| NFR-05-02 | Dashboard must be readable in direct sunlight (high-contrast mode) |
| NFR-05-03 | Configuration file format must be documented with examples |

---

**TODOs**

- [ ] Review and validate requirements with stakeholders
- [ ] Define acceptance criteria for each requirement
- [ ] Map requirements to test cases
- [ ] Add CAN FD and automotive Ethernet requirements in Phase 5
