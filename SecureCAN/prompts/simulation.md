# SecureCAN Attack Simulation Prompt

## Context

You are building the attack simulation engine for SecureCAN — an offline tool for security researchers and vehicle owners to test detection efficacy against known CAN attack patterns using recorded or live CAN data.

## Architecture

- **Location**: Mobile app service layer
- **Modes**: Offline-recorded, offline-synthetic, live-monitor, live-inject
- **MVP Mode**: Offline-recorded and offline-synthetic only (no live injection)
- **Scenario Format**: JSON (defined in `configs/attack_library.json`)

## Key Files to Reference

- `docs/ATTACK_SIMULATOR.md` — Full attack simulator specification
- `docs/THREAT_MODEL.md` — Threat model driving detection rules
- `configs/attack_library.json` — Pre-built attack scenarios

## Key Components

### Scenario Interpreter

Parses attack scenario definitions and produces a sequence of CAN frame modifications:

```typescript
interface AttackAction {
  type: 'inject' | 'modify' | 'drop' | 'delay' | 'replay';
  parameters: {
    canId?: number;
    canIdMask?: number;
    data?: string;
    dataPattern?: object;
    startDelayMs?: number;
    intervalMs?: number;
    count?: number;
    frequencyHz?: number;
  };
}
```

### Frame Source

Provides the base CAN frame stream:
- **Recorded**: Replay from SQLite `can_frames` table
- **Synthetic**: Generate frames matching vehicle profile

### Injection Engine

Applies attack actions to frame stream:
- Modifies frame data, timing, or sequence
- Injects new frames
- Drops or delays existing frames
- Passes modified stream to detection engine

### Results Collector

Compares detection results against expected outcomes:

```typescript
interface SimulationResult {
  scenarioId: string;
  framesProcessed: number;
  framesInjected: number;
  detections: {
    expectedAlert: string;
    expectedSeverity: string;
    triggered: boolean;
    actualSeverity: string;
    latencyMs: number;
  }[];
  summary: {
    detectionRate: number;
    falsePositives: number;
    falseNegatives: number;
    averageLatencyMs: number;
  };
}
```

## Adding a New Attack Scenario

1. Define scenario JSON in `configs/attack_library.json`
2. Ensure detection rules in `configs/firewall_rules.json` cover the attack
3. Test with recorded CAN session
4. Verify expected detection results match actual

## Simulation Report

Generate a complete report including:
- Scenario name and description
- Attack action sequence
- Frame processing statistics
- Detection comparison (expected vs actual)
- Timeline visualisation
- Recommendations for improving detection

---

**TODOs**

- [ ] Build synthetic CAN frame generator
- [ ] Implement scenario interpreter with all action types
- [ ] Create simulation results visualisation
- [ ] Add custom scenario editor UI
- [ ] Build regression test suite for all scenarios
