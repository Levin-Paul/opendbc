# Testing Strategy — SecureCAN

## Purpose

Define the testing strategy, test levels, test tools, and acceptance criteria for the SecureCAN platform.

## Scope

This document covers all testing activities for the SecureCAN mobile application, gateway firmware, hardware, and integration testing. It defines unit, integration, system, acceptance, and security testing.

## Test Levels

```
                         ┌─────────────────────┐
                         │   User Acceptance   │
                         │   Testing (UAT)     │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │   System Testing     │
                         │   (E2E, Performance) │
                         └──────────┬──────────┘
                                    │
               ┌────────────────────┼────────────────────┐
               │                    │                    │
     ┌─────────▼─────────┐ ┌────────▼───────┐ ┌────────▼────────┐
     │ Integration Tests  │ │ Security Tests  │ │  Hardware Tests │
     │ (Adapter, BLE, DB) │ │ (Auth, Fuzz)    │ │ (CAN, BLE, PWR)│
     └─────────┬─────────┘ └────────┬───────┘ └────────┬────────┘
               │                    │                    │
     ┌─────────▼─────────┐         │                    │
     │   Unit Tests       │         │                    │
     │ (Services, Models) │         │                    │
     └───────────────────┘         │                    │
                                    │                    │
     ┌──────────────────────────────┴────────────────────┘
     │   Firmware Tests (ESP-IDF test framework)
     └───────────────────────────────────────────────────
```

## Unit Testing

### Mobile App (TypeScript)

| Tool | Jest with ts-jest |
|------|-------------------|
| Coverage Target | 80% line, 70% branch |
| Location | `src/__tests__/` |
| Run Command | `npm run test` |

**Test Areas:**

- Service layer functions (BLEService, DecoderService, etc.)
- Rule evaluator engine (firewall, detection)
- Decoder Adapter Layer (signal decoding, edge cases)
- Database operations (CRUD, migrations)
- Utility functions (signal validation, CRC, serialisation)

### Gateway Firmware (C)

| Tool | Unity test framework (via ESP-IDF) |
|------|------------------------------------|
| Coverage Target | 70% line |
| Location | `firmware/esp32/test/` |
| Run Command | `idf.py test` |

**Test Areas:**

- CAN frame buffer (ring buffer operations, overflow)
- Protocol serialisation/deserialisation
- Authentication engine (sign/verify)
- Configuration storage (NVS read/write)
- CRC8 calculation

## Integration Testing

### Adapter Integration

- **OpenDBC Decoder Test**: Load each supported DBC file, feed known CAN frames, verify decoded signal values
- **BLE Protocol Test**: Simulate gateway and app, verify message exchange per API_SPEC.md
- **Database Migration Test**: Run all migrations on fresh database, verify schema version

### Test Fixtures

```
tests/fixtures/
  can_frames/              # Recorded CAN frame captures
    honda_civic_2020.json
    toyota_camry_2021.json
    vw_golf_2019.json
  decoder_output/          # Expected decoded values for fixtures
    honda_civic_2020_expected.json
  attack_scenarios/        # Attack scenario test inputs
    injection_test.json
    replay_test.json
  configs/                 # Test configuration files
    test_firewall_rules.json
    test_maintenance_rules.json
```

## System Testing

### End-to-End Tests

Simulate complete user flows using mocked gateway:

| Test | Description |
|------|-------------|
| Full Monitoring Flow | Connect, receive frames, decode, display |
| Alert Generation | Inject attack frames, verify alert creation |
| Authentication Flow | Pair, authenticate, verify session |
| Configuration Change | Modify firewall rule, verify enforcement |
| Data Export | Export alerts, verify CSV/JSON format |

### Performance Tests

| Test | Target | Tooling |
|------|--------|---------|
| CAN frame throughput (Wi-Fi) | 5000 frames/s sustained | Frame generator |
| BLE alert delivery latency | < 200 ms p99 | BLE sniffer |
| App cold start | < 3 seconds | React Native profiler |
| Database query (100K rows) | < 100 ms | SQLite benchmark |
| Memory usage (30 min session) | < 200 MB | Xcode/Android Studio |

## Security Testing

### Penetration Testing

| Area | Technique | Frequency |
|------|-----------|-----------|
| BLE Stack | BlueZ btlejack, Crackle | Per release |
| Firmware | ESP32 flash dump analysis | Per release |
| Mobile App | Frida, Objection, static analysis | Per major release |
| Communication | Man-in-the-middle proxy | Per release |
| Authentication | Replay, timing, brute force | Per release |

### Fuzz Testing

| Target | Tool | Input |
|--------|------|-------|
| CAN Frame Parser | Custom fuzzer | Malformed CAN frames |
| BLE Protocol | Boofuzz | Invalid message types |
| Config File Parser | Custom fuzzer | Malformed JSON |
| DBC File Parser | Custom fuzzer | Malformed DBC files |

## Hardware Testing

| Test | Method | Acceptance |
|------|--------|------------|
| CAN Loopback | TX → RX on bench | 100% frame accuracy |
| BLE Range | Open field testing | ≥ 10 m line of sight |
| Power Consumption | Current measurement | ≤ 350 mA active |
| Temperature | Thermal chamber | -20°C to +70°C operation |
| Vibration | SAE J1455 profile | No intermittent failures |
| ESD | IEC 61000-4-2 | ±8 kV contact, ±15 kV air |

## Acceptance Criteria

### MVP Acceptance

1. All unit tests pass (≥ 80% coverage)
2. All integration tests pass
3. Performance targets met (within 20% margin)
4. Security penetration test: no critical findings
5. Hardware validation: all electrical tests pass
6. BLE authentication: 100/100 successful attempts
7. CAN frame decoding: 99.9% accuracy vs. ground truth
8. Alert generation: zero false negatives on known attacks (lab environment)

## CI/CD Pipeline

```
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│  Lint    │→ │  Unit    │→ │Integrate │→ │  Build   │→ │  Deploy  │
│ (ESLint) │  │ (Jest)   │  │ (Tests)  │  │ (App/FW) │  │ (Test)   │
└──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘
```

- All pushes to `develop` run lint + unit tests
- All pushes to `main` run full pipeline
- Release branches require all tests passing + security review sign-off

---

**TODOs**

- [ ] Set up CI pipeline with GitHub Actions
- [ ] Create test fixture CAN frame captures for 3 vehicles
- [ ] Build BLE gateway simulator for integration tests
- [ ] Implement automated fuzz testing in CI
- [ ] Write hardware test automation scripts
