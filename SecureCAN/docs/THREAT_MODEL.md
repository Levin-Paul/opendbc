# Threat Model — SecureCAN

## Purpose

Identify, classify, and document threats against the SecureCAN platform. This document drives detection rule development, attack simulation scenarios, and security test cases.

## Scope

This threat model covers the SecureCAN system including the vehicle CAN bus, the gateway, the mobile application, communication channels, and the user's device. It uses STRIDE methodology.

## Methodology

- **Asset Identification** — Data and components requiring protection
- **Threat Enumeration** — STRIDE per component
- **Risk Assessment** — Likelihood × Impact matrix
- **Mitigation Mapping** — Controls mapped to each threat

## Assets

| Asset ID | Asset | Confidentiality | Integrity | Availability |
|----------|-------|----------------|-----------|--------------|
| A-01 | CAN bus messages | Low | High | Medium |
| A-02 | Decoded vehicle signals | Medium | High | Medium |
| A-03 | ECU fingerprints | Medium | High | Low |
| A-04 | User authentication keys | High | High | Low |
| A-05 | Gateway firmware | Low | High | High |
| A-06 | Firewall configuration | Medium | High | Low |
| A-07 | Maintenance predictions | Low | Medium | Low |
| A-08 | Attack signatures | Medium | High | Low |
| A-09 | Session keys | High | High | Medium |
| A-10 | User export data | User-defined | High | Low |

## STRIDE Threat Analysis

### Vehicle CAN Bus

| Threat | Description | Risk | Mitigation |
|--------|-------------|------|------------|
| **Spoofing** | Attacker sends messages impersonating a legitimate ECU | High | ECU fingerprinting, message frequency analysis, signal plausibility checks |
| **Tampering** | Attacker modifies CAN messages in transit | High | CRC validation, signal range checks, cross-signal verification |
| **Repudiation** | ECU denies sending a message | Medium | CAN frame logging with timestamps |
| **Information Disclosure** | Attacker reads CAN traffic via physical access | High | N/A (CAN bus is broadcast by design) — detection not prevention |
| **Denial of Service** | Attacker floods bus with high-priority messages (bus-off attack) | High | Bus-off detection, message frequency monitoring, CAN firewall |
| **Elevation of Privilege** | Attacker uses compromised ECU to send diagnostic commands | High | Message ID filtering, unexpected service request detection |

### SecureCAN Gateway

| Threat | Description | Risk | Mitigation |
|--------|-------------|------|------------|
| **Spoofing** | Fake gateway paired with user app | High | Ed25519 challenge-response authentication |
| **Tampering** | Gateway firmware modified by attacker | High | Signed firmware updates, bootloader verification |
| **Repudiation** | Gateway denies having forwarded a CAN frame | Medium | Forwarded frame logging with sequence numbers |
| **Information Disclosure** | Gateway leaks decrypted CAN data | Medium | All storage on mobile device, gateway buffers in RAM only |
| **Denial of Service** | Gateway crashes due to malformed CAN traffic | Medium | Watchdog timer, input validation, error frame handling |
| **Elevation of Privilege** | Write-enable bypass | Critical | Hardware DIP switch, TWAI listen-only mode enforced at hardware level |

### BLE/Wi-Fi Communication

| Threat | Description | Risk | Mitigation |
|--------|-------------|------|------------|
| **Spoofing** | Attacker impersonates gateway or app | High | BLE 5.0 LE Secure Connections, Ed25519 handshake |
| **Tampering** | Attacker modifies frames in transit | High | Encrypted link, frame sequence numbers, MAC verification |
| **Repudiation** | Gateway or app denies sending data | Low | Sequence numbers and session logging |
| **Information Disclosure** | Eavesdropping on BLE traffic | High | Mandatory encryption, no plaintext fallback |
| **Denial of Service** | BLE jammer disrupts communication | Medium | Wi-Fi fallback transport, local buffering |
| **Elevation of Privilege** | Attacker uses captured session to send commands | Medium | Session timeout, key rotation |

### Mobile Application

| Threat | Description | Risk | Mitigation |
|--------|-------------|------|------------|
| **Spoofing** | Malicious app pretending to be SecureCAN | High | OS-level app signing, cryptographic binding to gateway |
| **Tampering** | App binary modified to exfiltrate data | High | Code signing, runtime integrity checks (optional) |
| **Repudiation** | App denies having generated an alert | Low | Alert logging with local timestamps |
| **Information Disclosure** | Malware on device reads SecureCAN database | High | iOS Keychain / Android Keystore for keys, SQLite encryption (optional) |
| **Denial of Service** | App crashes on malformed gateway data | Medium | Input validation, error handling |
| **Elevation of Privilege** | Attacker uses rooted/jailbroken device to extract keys | Medium | Platform security features (Secure Enclave / TEE) when available |

## Risk Matrix

| Risk Level | Likelihood | Impact | Examples |
|------------|------------|--------|----------|
| **Critical** | High | High | Bus-off attack causing vehicle instability |
| **High** | Medium | High | ECU spoofing leading to incorrect alerts |
| **Medium** | High | Medium | BLE disconnection during monitoring |
| **Low** | Low | Low | Export file contains non-sensitive metadata |

## Attack Scenarios

### AS-01 — CAN Injection via OBD-II Port
An attacker with physical access to the OBD-II port connects a device that injects fake CAN messages. SecureCAN detects this through message frequency anomalies and unexpected CAN IDs.

### AS-02 — Replay Attack
An attacker records CAN traffic and replays it to trigger unintended behaviour. SecureCAN detects replay through message sequence analysis and unexpected signal value transitions.

### AS-03 — ECU Spoofing
An attacker's device sends messages with a legitimate ECU's CAN ID. SecureCAN detects spoofing through ECU fingerprint deviation and signal plausibility failures.

### AS-04 — Bus-Off Attack
An attacker floods the bus with error frames to force ECUs into bus-off state. SecureCAN detects bus-off via error frame count thresholds and unexpected silence from ECUs.

### AS-05 — Firmware Tampering
An attacker attempts to flash modified firmware to the SecureCAN Gateway. SecureCAN prevents this through signed update verification and bootloader integrity checks.

### AS-06 — Man-in-the-Middle (BLE)
An attacker attempts to intercept BLE communication between the app and gateway. SecureCAN mitigates this through BLE 5.0 LE Secure Connections encryption and the Ed25519 authentication handshake.

---

**TODOs**

- [ ] Map each threat to specific detection rule(s) in attack_library.json
- [ ] Create test harness for each attack scenario
- [ ] Conduct annual threat model review
- [ ] Add CAN FD and automotive Ethernet threats in Phase 5
