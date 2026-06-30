# Attack Simulator — SecureCAN

## Purpose

Define the architecture, scenario format, execution engine, and output reporting for the offline attack simulation capability.

## Scope

This document covers the attack simulation engine that operates within the mobile application, enabling security researchers and vehicle owners to test detection efficacy against known attack patterns using recorded or live CAN data.

## Architecture

```
┌───────────────────────────────────────────────────────────┐
│                 Attack Simulator Engine                      │
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ Scenario     │    │ Scenario     │    │ Injection    │  │
│  │ Library      │───→│ Interpreter  │───→│ Engine       │  │
│  └──────────────┘    └──────────────┘    └──────┬───────┘  │
│                                                  │          │
│  ┌──────────────┐    ┌──────────────┐           │          │
│  │ CAN Frame    │    │ Frame        │           │          │
│  │ Source       │───→│ Modifier     │───────────┘          │
│  └──────────────┘    └──────────────┘                      │
│                                                  │          │
│  ┌───────────────────────────────────────────────▼───────┐  │
│  │              Detection Engine Observer                   │  │
│  └───────────────────────────────────────────────────────┘  │
│                              │                               │
│  ┌───────────────────────────▼───────────────────────────┐  │
│  │              Results & Report Generator                  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Scenario Format

Attack scenarios are defined in JSON and stored in `configs/attack_library.json`. Each scenario specifies one or more attack actions.

### Scenario Schema

```json
{
  "scenario_id": "string — unique identifier",
  "name": "string — human-readable name",
  "description": "string — explanation of the attack scenario",
  "category": "injection | replay | spoofing | bus_off | diagnostic | custom",
  "difficulty": "beginner | intermediate | advanced",
  "estimated_duration_ms": "integer — estimated execution time",
  "attack_actions": [
    {
      "type": "inject | modify | drop | delay | replay",
      "parameters": {
        "can_id": "integer — target CAN ID",
        "can_id_mask": "integer — bitmask for matching",
        "data": "hex string — data to inject (for injection type)",
        "data_pattern": "object — pattern for modification (for modify type)",
        "start_delay_ms": "integer — delay before first action",
        "interval_ms": "integer — interval between repeated actions",
        "count": "integer — number of repetitions (0 = infinite)",
        "frequency_hz": "number — injection frequency"
      }
    }
  ],
  "expected_detection": {
    "should_trigger": "boolean — whether detection is expected",
    "alert_severity": "INFO | WARNING | CRITICAL | EMERGENCY",
    "alert_count": "integer — expected number of alerts"
  }
}
```

## Attack Scenarios Library

### SC-01 — CAN Injection — Arbitrary ID

Injects messages with a CAN ID that does not normally appear on the vehicle's bus.

```json
{
  "scenario_id": "SC-01",
  "name": "Arbitrary CAN ID Injection",
  "description": "Simulates an attacker injecting messages with a CAN ID not observed in the baseline. Tests detection of novel CAN IDs on the bus.",
  "category": "injection",
  "difficulty": "beginner",
  "estimated_duration_ms": 5000,
  "attack_actions": [
    {
      "type": "inject",
      "parameters": {
        "can_id": 2048,
        "data": "AABBCCDDEEFF0011",
        "start_delay_ms": 1000,
        "interval_ms": 100,
        "count": 50,
        "frequency_hz": 10
      }
    }
  ],
  "expected_detection": {
    "should_trigger": true,
    "alert_severity": "WARNING",
    "alert_count": 1
  }
}
```

### SC-02 — CAN Injection — Suspended ID

Injects messages using a legitimate CAN ID that already exists on the bus.

```json
{
  "scenario_id": "SC-02",
  "name": "Suspended CAN ID Injection",
  "description": "Simulates an attacker injecting additional messages using a CAN ID that belongs to a legitimate ECU. Tests detection of frequency anomalies.",
  "category": "injection",
  "difficulty": "beginner",
  "estimated_duration_ms": 5000,
  "attack_actions": [
    {
      "type": "inject",
      "parameters": {
        "can_id": 1050,
        "data": "AABBCCDDEEFF0011",
        "start_delay_ms": 1000,
        "interval_ms": 10,
        "count": 200,
        "frequency_hz": 100
      }
    }
  ],
  "expected_detection": {
    "should_trigger": true,
    "alert_severity": "WARNING",
    "alert_count": 1
  }
}
```

### SC-03 — Replay Attack

Records CAN messages and replays them back onto the bus.

```json
{
  "scenario_id": "SC-03",
  "name": "CAN Replay Attack",
  "description": "Simulates an attacker recording CAN traffic and replaying it. Tests detection of replayed messages through sequence analysis and timing.",
  "category": "replay",
  "difficulty": "intermediate",
  "estimated_duration_ms": 10000,
  "attack_actions": [
    {
      "type": "replay",
      "parameters": {
        "source_session_id": "integer — session to replay from",
        "start_position": 0,
        "count": 100,
        "speed_multiplier": 1.0,
        "loop": false
      }
    }
  ],
  "expected_detection": {
    "should_trigger": true,
    "alert_severity": "WARNING",
    "alert_count": 1
  }
}
```

### SC-04 — Bus-Off Attack

Floods the bus with dominant bits to force ECUs into bus-off state.

```json
{
  "scenario_id": "SC-04",
  "name": "Bus-Off Attack (Error Frame Flood)",
  "description": "Simulates an attacker flooding the bus with error frames to force ECUs into bus-off state. Tests detection of bus-off conditions and abnormal error frame counts.",
  "category": "bus_off",
  "difficulty": "advanced",
  "estimated_duration_ms": 8000,
  "attack_actions": [
    {
      "type": "inject",
      "parameters": {
        "can_id": 0,
        "data": "0000000000000000",
        "start_delay_ms": 2000,
        "interval_ms": 1,
        "count": 5000,
        "frequency_hz": 1000
      }
    }
  ],
  "expected_detection": {
    "should_trigger": true,
    "alert_severity": "EMERGENCY",
    "alert_count": 3
  }
}
```

### SC-05 — ECU Spoofing — ID Takeover

Attacker sends messages with a legitimate ECU's ID while the real ECU is quiet.

```json
{
  "scenario_id": "SC-05",
  "name": "ECU Spoofing — ID Takeover",
  "description": "Simulates an attacker suppressing a legitimate ECU's messages and injecting their own messages with the same CAN ID. Tests ECU fingerprint deviation detection.",
  "category": "spoofing",
  "difficulty": "advanced",
  "estimated_duration_ms": 15000,
  "attack_actions": [
    {
      "type": "inject",
      "parameters": {
        "can_id": 1050,
        "data_pattern": "FFFFFFFFFFFFFFFF",
        "start_delay_ms": 5000,
        "interval_ms": 10,
        "count": 100,
        "frequency_hz": 100
      }
    }
  ],
  "expected_detection": {
    "should_trigger": true,
    "alert_severity": "CRITICAL",
    "alert_count": 2
  }
}
```

## Execution Engine

### Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| **Offline — Recorded** | Replay against recorded CAN session | Testing detection rules against known data |
| **Offline — Synthetic** | Generate and inject synthetic CAN frames | Testing without vehicle connected |
| **Live — Monitor** | Observe live CAN traffic, detect scenario matches | Real-time alert verification |
| **Live — Inject** | Inject attack frames into live CAN (requires write-enable) | Advanced testing (disabled in MVP) |

### Execution Flow

```
1. User selects scenario from library
2. User selects data source (recorded session or synthetic)
3. Scenario Interpreter parses attack_actions
4. Frame Source provides CAN frames (recorded or generated)
5. Frame Modifier applies attack actions to frame stream
6. Injection Engine sends modified stream to Detection Engine
7. Detection Engine processes frames as if from live traffic
8. Results Collector records all alerts, matches against expected
9. Report Generator produces comparison report
```

## Results Reporting

### Report Format

```json
{
  "simulation_id": "uuid",
  "scenario_id": "SC-01",
  "scenario_name": "Arbitrary CAN ID Injection",
  "started_at": "2026-06-30T12:00:00Z",
  "completed_at": "2026-06-30T12:00:05Z",
  "frames_processed": 5000,
  "frames_injected": 50,
  "detection_results": [
    {
      "expected_alert": "Novel CAN ID detected",
      "expected_severity": "WARNING",
      "triggered": true,
      "actual_severity": "WARNING",
      "latency_ms": 45,
      "matched_rule": "fw_novel_can_id"
    }
  ],
  "summary": {
    "total_expected_alerts": 1,
    "total_triggered_alerts": 1,
    "detection_rate": 1.0,
    "false_positives": 0,
    "false_negatives": 0,
    "average_latency_ms": 45
  }
}
```

---

**TODOs**

- [ ] Implement Scenario Interpreter with JSON parsing
- [ ] Build pre-built scenario library (expand from 8 MVP scenarios to 20+ for Phase 3)
- [ ] Create synthetic CAN frame generator for offline testing
- [ ] Implement results report generator with visual diff
- [ ] Add custom scenario editor UI in mobile app
