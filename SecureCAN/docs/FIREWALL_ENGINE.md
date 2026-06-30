# CAN Firewall Engine — SecureCAN

## Purpose

Define the architecture, rule format, evaluation logic, and integration of the CAN firewall engine within the SecureCAN platform.

## Scope

This document covers the firewall engine that operates in the mobile application layer. The MVP operates in monitor-only mode — rules are evaluated against CAN traffic and violations generate alerts, but no CAN messages are blocked at the hardware level.

## Architecture

```
┌─────────────────────────────────────────────┐
│              CAN Firewall Engine              │
│                                               │
│  ┌──────────┐    ┌────────────────────┐      │
│  │ Rule     │    │  Frame Pre-        │      │
│  │ Loader   │───→│  processor         │      │
│  └──────────┘    └────────┬───────────┘      │
│                           │                   │
│                  ┌────────▼───────────┐      │
│                  │  Rule Evaluator    │      │
│                  │  (multi-pass)      │      │
│                  └────────┬───────────┘      │
│                           │                   │
│                  ┌────────▼───────────┐      │
│                  │  Action Dispatcher │      │
│                  └────────┬───────────┘      │
│                           │                   │
│                  ┌────────▼───────────┐      │
│                  │  Log / Alert       │      │
│                  │  Generator         │      │
│                  └────────────────────┘      │
└─────────────────────────────────────────────┘
```

## Rule Format

Firewall rules are defined in JSON format and stored in `configs/firewall_rules.json`. Each rule contains:

### Schema

```json
{
  "rule_id": "string — unique identifier",
  "name": "string — human-readable name",
  "description": "string — explanation of what this rule detects",
  "enabled": "boolean",
  "priority": "integer — 0 (highest) to 100 (lowest)",
  "action": "allow | block | drop | alert",
  "conditions": {
    "can_id": {
      "value": "integer — exact CAN ID to match",
      "mask": "integer — bitmask for ID matching (0x7FF for 11-bit, 0x1FFFFFFF for 29-bit)",
      "match": "exact | range | any"
    },
    "can_id_range": {
      "min": "integer",
      "max": "integer"
    },
    "data_pattern": {
      "offset": "integer — byte offset in data",
      "value": "integer — expected value at offset",
      "mask": "integer — bitmask",
      "match": "exact | any | not"
    },
    "frequency": {
      "max_per_second": "number — maximum messages per second",
      "window_ms": "integer — sliding window in milliseconds"
    },
    "dlc": {
      "value": "integer — expected data length code",
      "match": "exact | min | max"
    },
    "bus": {
      "value": "integer — CAN bus number"
    }
  },
  "alert": {
    "severity": "INFO | WARNING | CRITICAL | EMERGENCY",
    "title": "string — alert title template",
    "description": "string — alert description template",
    "category": "threat"
  }
}
```

### Example Rules

**Rule 1: Block diagnostic messages from unknown sources**
```json
{
  "rule_id": "fw_block_diag_unknown",
  "name": "Block Unknown Diagnostic Messages",
  "description": "Blocks diagnostic CAN messages (0x7DF-0x7EF) from unrecognised sources",
  "enabled": true,
  "priority": 10,
  "action": "alert",
  "conditions": {
    "can_id": {
      "mask": 0x7F8,
      "value": 0x7D8,
      "match": "range"
    }
  },
  "alert": {
    "severity": "CRITICAL",
    "title": "Diagnostic Message Detected",
    "description": "A diagnostic request (CAN ID {can_id}) was detected. This may indicate a scan tool or unauthorised diagnostic access.",
    "category": "threat"
  }
}
```

**Rule 2: Rate-limit high-priority messages**
```json
{
  "rule_id": "fw_rate_limit_high",
  "name": "Rate Limit High-Priority Messages",
  "description": "Alerts when any single CAN ID exceeds 100 messages per second",
  "enabled": true,
  "priority": 20,
  "action": "alert",
  "conditions": {
    "frequency": {
      "max_per_second": 100,
      "window_ms": 1000
    }
  },
  "alert": {
    "severity": "WARNING",
    "title": "High Message Rate Detected",
    "description": "CAN ID {can_id} transmitted {count} messages in 1 second (limit: 100). This may indicate a bus flood or malfunctioning ECU.",
    "category": "threat"
  }
}
```

**Rule 3: Allow known ECU messages**
```json
{
  "rule_id": "fw_allow_known_ecu",
  "name": "Allow Known ECU Messages",
  "description": "Allows messages from known ECU CAN IDs in the vehicle profile",
  "enabled": true,
  "priority": 0,
  "action": "allow",
  "conditions": {
    "can_id": {
      "match": "any"
    }
  }
}
```

## Rule Evaluation

### Evaluation Order

1. Rules are sorted by priority (ascending)
2. Each incoming CAN frame is evaluated against all enabled rules
3. The first matching rule determines the action
4. If no rule matches, the default action is `allow` with no alert

### Performance Requirements

- Single frame evaluation: ≤ 10 µs on mobile device CPU
- Rule set size: up to 500 rules without measurable latency
- Memory: rule set loaded as immutable array, ~2 KB per rule

## Actions

| Action | MVP Behaviour | Future Behaviour |
|--------|---------------|------------------|
| `allow` | No alert, frame processed normally | Frame forwarded |
| `alert` | Alert generated, frame processed normally | Alert generated, frame processed normally |
| `block` | N/A (read-only MVP) | Frame not forwarded to app |
| `drop` | N/A (read-only MVP) | Frame not forwarded, no alert |

## Rule Management

- Rules are loaded from `configs/firewall_rules.json` at app start
- Users can add custom rules via Settings → Firewall → Add Rule
- Custom rules are stored in SQLite `config` table with key `firewall_custom_rules`
- Rule changes take effect immediately without app restart
- Export/import of firewall configuration supported

---

**TODOs**

- [ ] Implement rule evaluator with multi-pass matching
- [ ] Build rule editor UI in Settings screen
- [ ] Add rule statistics (match count, last matched timestamp)
- [ ] Implement rule testing mode with historical data replay
- [ ] Define hardware firewall integration for Phase 3 write-capable gateway
