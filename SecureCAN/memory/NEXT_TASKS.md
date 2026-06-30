# Next Tasks

This file lists the next high-priority tasks beyond the current sprint backlog. Tasks are ordered by priority.

## Immediate (Next Sprint)

| Priority | Task | Owner | Notes |
|----------|------|-------|-------|
| P0 | Set up React Native project scaffold | TBD | Initialize with TypeScript strict mode |
| P0 | Set up ESP-IDF project for gateway firmware | TBD | Target ESP32-S3 |
| P0 | Initialize OpenDBC git submodule | TBD | Pin to specific commit |
| P1 | Build CAN frame capture firmware module | TBD | TWAI controller, ring buffer |
| P1 | Build BLE GATT service firmware module | TBD | Service + characteristics |
| P1 | Build BLE client service in mobile app | TBD | react-native-ble-plx integration |
| P1 | Implement BaseDecoder abstract class | TBD | TypeScript decoder adapter |
| P1 | Implement HondaAdapter vehicle decoder | TBD | First vehicle adapter |
| P2 | Build Dashboard screen with signal cards | TBD | Real-time display |
| P2 | Implement Ed25519 authentication in firmware | TBD | Key generation, signing |
| P2 | Implement authentication flow in app | TBD | Challenge-response handshake |

## Short-Term (This Phase)

| Priority | Task | Owner | Notes |
|----------|------|-------|-------|
| P2 | Write CI pipeline (GitHub Actions) | TBD | Lint, test, build |
| P2 | Create test fixture CAN captures | TBD | At least 3 vehicles |
| P3 | Build gateway simulator for app testing | TBD | BLE mock or TCP simulator |
| P3 | Write integration tests for decoder adapter | TBD | DBC loading + decoding |
| P3 | Set up firmware signing infrastructure | TBD | Dev and prod keys |

## Medium-Term (Next Phase)

| Priority | Task | Owner | Notes |
|----------|------|-------|-------|
| P1 | Implement threat detection engine | TBD | Rule matching + alerts |
| P1 | Implement CAN firewall rule evaluator | TBD | JSON rule processing |
| P2 | Implement ECU fingerprinting | TBD | Feature collection + hashing |
| P2 | Implement predictive maintenance for battery | TBD | Linear regression trend |
| P3 | Build Alert screen with filtering | TBD | Severity, category, search |
| P3 | Implement configuration file import/export | TBD | JSON file handling |

## Long-Term (Phase 2+)

| Priority | Task | Owner | Notes |
|----------|------|-------|-------|
| P2 | Implement attack simulation engine | TBD | Scenario interpreter |
| P3 | Build fleet multi-vehicle dashboard | TBD | Vehicle list + aggregate view |
| P3 | Add CAN FD support to gateway | TBD | MCP2517FD controller |
| P4 | Automotive Ethernet support | TBD | 100BASE-T1 PHY |

---

**TODOs**

- [ ] Assign owners to all P0 and P1 tasks
- [ ] Estimate effort for top 10 tasks
- [ ] Move top P0 tasks to next sprint backlog
