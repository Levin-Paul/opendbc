# User Flow — SecureCAN

## Purpose

Document the primary user flows through the SecureCAN platform, from initial setup through daily monitoring and maintenance.

## Scope

This document covers the complete user journey for three primary user personas: vehicle owner, fleet operator, and security researcher. Each flow includes screens, decision points, error states, and success criteria.

## Persona 1 — Vehicle Owner

### Flow 1.1 — First-Time Setup

```
Start
  │
  ▼
[App Launch] ──First launch?──→ Yes ──→ [Onboarding Screen]
  │                                        │
  │                                        │ Welcome, privacy notice,
  │                                        │ offline-first explanation
  │                                        │
  │                                        ▼
  │                                     [Key Generation]
  │                                        │
  │                                        │ Generate Ed25519 keypair
  │                                        │ Store private key in OS Keychain
  │                                        │ Display public key as QR code
  │                                        │
  │                                        ▼
  │                                     [Gateway Pairing]
  │                                        │
  │                                        │ Scan QR code on gateway
  │                                        │ BLE handshake
  │                                        │ Public key exchange
  │                                        │
  │                                        ▼
  │                                     [Vehicle Profile]
  │                                        │
  │                                        │ Select make/model/year
  │                                        │ OR auto-detect via VIN
  │                                        │ OpenDBC fingerprint match
  │                                        │
  │                                        ▼
  │                                     [Setup Complete]
  │                                        │
  └────────────── No ──────────────────────┘
                     │
                     ▼
              [Dashboard]
```

### Flow 1.2 — Daily Monitoring

```
[Dashboard]
  │
  ├── View live signals ──→ Signal cards update in real-time
  │
  ├── Review alerts ──→ Alert list filtered by severity
  │     │
  │     └── Tap alert ──→ Alert detail view
  │            │
  │            ├── Acknowledge ──→ Alert moves to acknowledged
  │            └── Recommended action ──→ Follow steps
  │
  ├── View CAN traffic ──→ Raw frame viewer with search/filter
  │
  └── Check connection ──→ Connection status indicator
         │
         ├── Connected ──→ Green indicator
         └── Disconnected ──→ Red indicator, retry button
```

### Flow 1.3 — Alert Acknowledgment

```
[Alert Notification]
  │
  ▼
[Alert Detail]
  │
  ├── Title: [Alert title]
  ├── Severity: [EMERGENCY/CRITICAL/WARNING/INFO]
  ├── Timestamp: [time]
  ├── Component: [affected ECU/sensor]
  ├── Description: [what happened]
  ├── Evidence: [data supporting detection]
  ├── Recommended Action: [what to do]
  │
  ├── [Acknowledge] ──→ Alert acknowledged, moves to history
  │
  └── [Export] ──→ Alert exported as JSON/PDF
```

### Flow 1.4 — Predictive Maintenance Check

```
[Maintenance Tab]
  │
  ├── Overview ──→ Summary of all monitored components
  │     ├── Battery: OK (12.6V, trending stable)
  │     ├── DPF: WARNING (pressure rising)
  │     └── Brakes: OK (estimated 15k km remaining)
  │
  └── Tap component ──→ Detail view
        │
        ├── Trend chart (30 days)
        ├── Current value vs. threshold
        ├── Prediction timeline
        └── Recommended maintenance interval
```

## Persona 2 — Fleet Operator

### Flow 2.1 — Multi-Vehicle Dashboard

```
[Fleet Dashboard]
  │
  ├── Vehicle list ──→ All vehicles in fleet
  │     ├── Vehicle 1: OK (3 alerts)
  │     ├── Vehicle 2: WARNING (maintenance due)
  │     └── Vehicle 3: CRITICAL (security alert)
  │
  ├── Tap vehicle ──→ Individual vehicle dashboard (same as owner)
  │
  └── Fleet health summary ──→ Aggregate stats
        ├── Total alerts by severity
        ├── Maintenance due count
        └── Last seen timestamps
```

## Persona 3 — Security Researcher

### Flow 3.1 — Attack Simulation

```
[Attack Simulator]
  │
  ├── Select scenario ──→ Scenario library
  │     ├── CAN Injection — Arbitrary ID
  │     ├── CAN Injection — Suspended ID
  │     ├── Replay Attack — Recorded Session
  │     ├── Bus-Off Attack — Error Frame Flood
  │     └── ECU Spoofing — ID Takeover
  │
  ├── Select target ──→ Choose recorded session or live
  │
  ├── Configure parameters ──→ Injection rate, CAN IDs, data pattern
  │
  ├── [Run Simulation] ──→ Simulation executes
  │     │
  │     └── Results ──→ Detection rate, alerts triggered, timeline
  │
  └── [Export Report] ──→ Full simulation report (JSON/PDF)
```

### Flow 3.2 — CAN Traffic Analysis

```
[Traffic Analyzer]
  │
  ├── Raw frame view ──→ All captured frames with filter
  │     ├── Filter by CAN ID
  │     ├── Filter by time range
  │     └── Filter by data pattern
  │
  ├── Statistics ──→ Bus utilisation, message rates per ID
  │
  └── Export ──→ Raw frame dump (CSV/JSON)
```

## Cross-Cutting Flows

### Flow C-01 — Configuration Import/Export

```
[Settings → Configuration]
  │
  ├── Export config ──→ JSON file saved to device storage
  │     ├── Firewall rules
  │     ├── Maintenance thresholds
  │     ├── Attack signatures
  │     └── Vehicle profile
  │
  └── Import config ──→ File picker → Validation → Apply
```

### Flow C-02 — Gateway Firmware Update

```
[Settings → Gateway → Firmware Update]
  │
  ├── Check version ──→ Current vs. latest
  │
  ├── Download update ──→ Firmware binary downloaded to phone
  │
  ├── Transfer to gateway ──→ BLE file transfer
  │     ├── Progress bar
  │     └── Verification ──→ Signature check on gateway
  │
  └── Apply update ──→ Gateway reboots → Reconnect
```

---

**TODOs**

- [ ] Create wireframes for each screen in the user flows
- [ ] Conduct usability testing with 5 beta users per persona
- [ ] Document error recovery flows for each failure mode
- [ ] Add fleet management flows for vehicle group operations
