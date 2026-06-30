# Component Verification — ECU & Sensor Integrity

## Purpose

Define the methods, algorithms, and procedures used to verify ECU identity and sensor integrity within the SecureCAN platform.

## Scope

This document covers ECU fingerprinting, ECU integrity snapshot and comparison, sensor plausibility checks, and component-level integrity verification.

## ECU Fingerprinting

### Overview

Each ECU on the CAN bus exhibits a unique behavioural fingerprint based on its message timing, data patterns, and responses to specific conditions. SecureCAN captures these characteristics to create a baseline identity for each ECU.

### Fingerprint Components

| Feature | Description | Weight |
|---------|-------------|--------|
| Message Frequency | Expected messages per second for each CAN ID | 0.30 |
| Message Periodicity | Inter-message timing variance | 0.25 |
| Data Value Ranges | Typical min/max values for each signal | 0.20 |
| Signal Transition Rate | Maximum rate of change for analog signals | 0.15 |
| CRC/Checksum Pattern | Algorithm identifier if determinable | 0.10 |

### Fingerprint Generation

```
For each CAN ID observed:
  1. Collect 1000+ message samples over normal driving cycle
  2. Calculate:
     a. Message count per second (mean, std dev)
     b. Inter-message interval histogram
     c. Per-signal min, max, mean, std dev
     d. Per-signal maximum delta between consecutive messages
  3. Hash feature vector into SHA-256 fingerprint
  4. Store fingerprint as baseline
```

### Fingerprint Format

```json
{
  "can_id": 1050,
  "is_extended": false,
  "name": "Engine ECU (ECM)",
  "fingerprint_hash": "a1b2c3d4e5f6...",
  "features": {
    "msg_frequency": {
      "mean": 100.0,
      "std_dev": 2.5
    },
    "inter_msg_interval": {
      "mean_ms": 10.0,
      "std_dev_ms": 0.5
    },
    "signals": [
      {
        "name": "engineSpeed",
        "min": 0,
        "max": 7000,
        "mean": 1500,
        "std_dev": 800,
        "max_delta": 500
      }
    ]
  },
  "created_at": "2026-06-30T12:00:00Z"
}
```

### Matching

When comparing a current observation against a baseline:

1. Compute deviation score for each feature
2. Weighted sum produces overall similarity score (0-1)
3. Thresholds:
   - ≥ 0.90: Match (ECU identity verified)
   - 0.70–0.89: Partial match (potential modification)
   - < 0.70: No match (ECU replaced or tampered)

## ECU Integrity Snapshot

### Overview

An integrity snapshot captures the full state of all observed ECUs at a point in time. Snapshots are used as trusted baselines for future comparisons.

### Snapshot Creation

```
1. Ensure vehicle is in known state (engine off, ignition on)
2. Observe CAN traffic for 60 seconds
3. Collect fingerprints for all observed ECUs
4. Record vehicle VIN and odometer (if available)
5. Hash entire snapshot into SHA-256 manifest hash
6. Present hash to user for optional external verification
```

### Snapshot Comparison

```
Baseline Snapshot (2026-05-01)       Current Observation (2026-06-30)
┌──────────────────────┐             ┌──────────────────────┐
│ ECU 0x100: hash A    │             │ ECU 0x100: hash A    │  ✓ Match
│ ECU 0x200: hash B    │             │ ECU 0x200: hash C    │  ✗ Changed
│ ECU 0x300: hash C    │             │ ECU 0x300: hash C    │  ✓ Match
│ ECU 0x400: hash D    │             │ ECU 0x400: ———       │  ✗ Missing
│                      │             │ ECU 0x500: hash E    │  ✗ New ECU
└──────────────────────┘             └──────────────────────┘

Changes detected: 3 of 4 ECUs changed
Verdict: INTEGRITY_FAILURE — review changes
```

### Alert Triggers

- New ECU appears on bus (CAN ID not in baseline)
- Known ECU disappears from bus (not observed for 5 consecutive windows)
- ECU fingerprint hash changed (ECU replaced or firmware updated)
- Multiple ECUs changed simultaneously (possible tampering event)

## Sensor Plausibility Checks

### Overview

Sensor plausibility validates that sensor readings make physical sense given the current vehicle state and other sensor readings.

### Plausibility Rules

| Rule | Description | Example |
|------|-------------|---------|
| Range Check | Sensor value within physical limits | Speed sensor: 0–320 km/h |
| Rate Check | Value changes within physical limits | RPM delta: ≤ 1000 per 100ms |
| Consistency | Correlated sensors agree | Speed vs. wheel speed sensors |
| Physical Limits | Value respects physics | Coolant temp: -40°C to 150°C |
| State Dependency | Value matches vehicle state | Engine off → RPM = 0 |

### Cross-Signal Validation

```
Vehicle Speed (50 km/h)          Wheel Speed FR (50 km/h)    ✓
                                  Wheel Speed FL (48 km/h)    ✓ (turning)
                                  Wheel Speed RR (50 km/h)    ✓
                                  Wheel Speed RL (52 km/h)    ✗ (ABS active or fault)

Brake Pressure (0 kPa)           Brake Light Switch (OFF)    ✓
                                  Deceleration (0.0 m/s²)    ✓

Engine RPM (2500)                Vehicle Speed (50 km/h)     Gear ratio calculation
                                  Transmission State (3rd)    ✓ (ratio matches)
```

### Alert Triggers

- Single sensor out of range → INFO alert
- Two correlated sensors disagree → WARNING alert
- Multiple sensors inconsistent → CRITICAL alert
- Impossible physical value → CRITICAL alert

## Component Integrity Verification Workflow

```
User triggers verification:
  1. Ensure vehicle in safe state (parked, ignition on)
  2. Begin observation period (60 seconds)
  3. Collect ECU fingerprints
  4. Run sensor plausibility checks
  5. Compare current fingerprints against baseline
  6. Generate verification report:
     a. ECU fingerprint results (match/changed/new/missing)
     b. Sensor plausibility results (pass/warning/fail)
     c. Overall integrity score
     d. Recommended actions for each finding
```

---

**TODOs**

- [ ] Validate fingerprint feature set against 10+ vehicle makes
- [ ] Implement fingerprint matching with configurable thresholds
- [ ] Build integrity snapshot comparison UI
- [ ] Define sensor plausibility rules database schema
- [ ] Create automated integrity verification test suite
