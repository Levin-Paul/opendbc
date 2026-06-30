# SecureCAN Testing Prompt

## Context

You are writing tests for SecureCAN — covering the React Native mobile app, ESP32 gateway firmware, and hardware validation.

## Testing Philosophy

1. **Test the safety-critical path** — Authentication, CAN decoding, detection rules
2. **Test offline behaviour** — No network required; mock all external dependencies
3. **Test edge cases** — Invalid CAN frames, malformed configurations, boundary values
4. **Test alert correctness** — Every detection rule must produce correct alerts

## Key Files to Reference

- `docs/TESTING.md` — Complete testing strategy
- `docs/SRS.md` — Requirements mapped to test cases
- `docs/API_SPEC.md` — Protocol conformance tests
- `configs/` — Configuration files used as test fixtures

## Test Levels

### Unit Tests (Jest, 80% coverage)

```
src/__tests__/
├── services/
│   ├── decoder.test.ts        # Signal decoding, edge cases
│   ├── threat-detection.test.ts  # Rule matching, alert generation
│   ├── firewall.test.ts       # Rule evaluation, priority ordering
│   ├── maintenance.test.ts    # Trend analysis, prediction
│   ├── ble-service.test.ts    # Protocol encode/decode
│   └── config.test.ts        # Config validation, file reading
├── utils/
│   ├── crc8.test.ts          # CRC8-ATM calculation
│   ├── serialisation.test.ts  # Binary format encode/decode
│   └── validation.test.ts    # Signal range, input validation
└── components/
    ├── SignalCard.test.ts
    ├── AlertCard.test.ts
    └── SeverityBadge.test.ts
```

### Integration Tests

```
tests/
├── integration/
│   ├── ble-protocol.test.ts    # Full message exchange simulation
│   ├── decoder-adapter.test.ts # DBC loading + frame decoding
│   ├── db-migration.test.ts    # Schema migration correctness
│   └── attack-simulator.test.ts# Scenario execution + detection
└── fixtures/
    ├── can_frames/             # Recorded CAN captures
    ├── decoder_output/         # Expected decoded values
    └── configs/                # Test configuration files
```

### Firmware Tests (Unity)

```
firmware/esp32/test/
├── test_can_controller.c      # TWAI init, frame RX
├── test_can_buffer.c          # Ring buffer push/pop, overflow
├── test_protocol.c            # Encode/decode binary messages
├── test_auth.c                # Ed25519 sign/verify
└── test_crc8.c               # CRC8 calculation
```

## Writing Test Cases

### Service Test Pattern

```typescript
describe('ThreatDetectionService', () => {
  beforeEach(() => {
    // Load test rules from fixtures
    // Clear detection state
  });

  test('detects novel CAN ID', () => {
    const frame = createFrame({ id: 0x999, data: '...' });
    const alerts = service.evaluate(frame);
    expect(alerts).toHaveLength(1);
    expect(alerts[0].severity).toBe('WARNING');
    expect(alerts[0].rule_id).toBe('fw_novel_can_id');
  });

  test('ignores known CAN ID', () => {
    const frame = createFrame({ id: 0x100, data: '...' });
    const alerts = service.evaluate(frame);
    expect(alerts).toHaveLength(0);
  });

  test('handles malformed frame gracefully', () => {
    const frame = createFrame({ id: -1, data: '' });
    expect(() => service.evaluate(frame)).not.toThrow();
  });
});
```

### Test Fixture Pattern

```typescript
// tests/fixtures/can_frames/honda_civic_2020.ts
export const hondaFrames: CanFrame[] = [
  { timestamp: 0, id: 0x158, isExtended: false, dlc: 8, data: Uint8Array.from([...]) },
  { timestamp: 10, id: 0x17C, isExtended: false, dlc: 8, data: Uint8Array.from([...]) },
  // ...
];

// Expected decoded values
export const hondaExpected: DecodedSignal[] = [
  { name: 'engineSpeed', value: 2450, unit: 'rpm' },
  { name: 'vehicleSpeed', value: 65, unit: 'km/h' },
  // ...
];
```

## CI Gate Rules

| Gate | Requirement |
|------|-------------|
| PR to develop | All unit tests pass, lint passes |
| PR to main | All tests pass, coverage ≥ 80%, security tests pass |
| Release | All tests pass, integration tests pass, hardware validation passes |

## Performance Benchmarks

Tests must verify:
- CAN frame decoding: ≤ 1 ms per frame
- Rule evaluation: ≤ 10 µs per frame
- Database query (100K rows): ≤ 100 ms
- BLE protocol encode/decode: ≤ 5 ms per message

---

**TODOs**

- [ ] Create test fixture CAN captures for all supported vehicles
- [ ] Build BLE gateway simulator for integration tests
- [ ] Add fuzz testing for protocol parser
- [ ] Implement performance benchmark suite
- [ ] Set up CI pipeline with GitHub Actions
