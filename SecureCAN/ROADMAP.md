# SecureCAN Roadmap

## Phase 0 — Foundation (Current)

**Q3 2026**

- [ ] ESP32 CAN bus gateway prototype with BLE streaming
- [ ] React Native app scaffold with BLE connectivity
- [ ] OpenDBC decoder adapter for 3 vehicle profiles
- [ ] Real-time signal dashboard (speed, RPM, coolant temp, etc.)
- [ ] CAN frame capture and local storage
- [ ] Basic authentication handshake (app ↔ gateway)
- [ ] Project documentation and constitution finalised

> **Vehicle support note:** `configs/supported_vehicles.json` lists all vehicles with OpenDBC DBC coverage (potential compatibility). Roadmap milestones reference adapters that have undergone real-vehicle validation. Vehicles listed as `verified` or `beta` in `supported_vehicles.json` may exceed the current roadmap adapter count.

## Phase 1 — MVP

**Q4 2026**

- [ ] ECU fingerprinting engine
- [ ] ECU integrity snapshot and comparison
- [ ] Sensor plausibility checks (cross-signal validation)
- [ ] Attack detection engine (injection, replay, spoofing, bus-off)
- [ ] CAN firewall rule engine (allow/block/drop)
- [ ] Predictive maintenance — battery voltage trend analysis
- [ ] Predictive maintenance — DPF pressure monitoring
- [ ] Alert notification system with severity levels
- [ ] Configuration file import/export
- [ ] Firmware OTA update mechanism
- [ ] Vehicle adapter for 5 additional makes/models

## Phase 2 — Integrity & Maintenance

**Q1 2027**

- [ ] Component integrity verification with cryptographic baselines
- [ ] Predictive maintenance — brake pad wear estimation
- [ ] Predictive maintenance — tyre pressure trend analysis
- [ ] Predictive maintenance — coolant temperature variance
- [ ] Fleet multi-vehicle dashboard
- [ ] Historical data replay and analysis
- [ ] Maintenance report export (PDF/CSV)
- [ ] Custom maintenance rule editor

## Phase 3 — Attack Simulation

**Q2 2027**

- [ ] Offline attack simulation engine
- [ ] Pre-built attack scenario library (expanded from 8 MVP scenarios to 20+)
- [ ] Simulation result report generation
- [ ] "What-if" analysis mode for security researchers
- [ ] Custom attack script editor
- [ ] Simulation replay against recorded CAN traffic

## Phase 4 — Advanced Features

**Q3 2027**

- [ ] CAN bus topology mapping
- [ ] ECU conversation analysis and profiling
- [ ] Statistical anomaly detection (ML-based baseline modelling)
- [ ] Optional encrypted cloud backup (user-managed key)
- [ ] Web dashboard (companion to mobile app)
- [ ] API for third-party integration
- [ ] Hardware Security Module (HSM) support for gateway

## Phase 5 — Scale

**Q4 2027**

- [ ] Vehicle adapter SDK for community contributions
- [ ] Plugin architecture for community detection rules
- [ ] CAN FD support
- [ ] Automotive Ethernet support
- [ ] Multi-gateway support for vehicles with multiple CAN buses
- [ ] OBD-II parameter ID (PID) auto-discovery
- [ ] Regulatory compliance documentation (ISO 21434, UN R155)

---

**TODOs**

- [ ] Review and adjust quarterly milestones based on MVP feedback
- [ ] Define exit criteria for each phase
- [ ] Publish public roadmap board
