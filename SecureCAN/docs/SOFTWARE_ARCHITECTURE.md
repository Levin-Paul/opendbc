# Software Architecture — SecureCAN Mobile App

## Purpose

Define the internal software architecture, component relationships, and design patterns used in the SecureCAN mobile application.

## Scope

This document covers the React Native mobile application, including the Decoder Adapter Layer, detection engines, storage layer, and UI components. Gateway firmware architecture is documented separately in HARDWARE_ARCHITECTURE.md.

## Architecture Pattern

The mobile app uses a **layered architecture** with unidirectional data flow:

```
┌─────────────────────────────────────────────────────┐
│                     UI Layer                         │
│  Dashboard | Alerts | Configuration | Maintenance   │
└───────────────────────┬─────────────────────────────┘
                        │ State updates
┌───────────────────────▼─────────────────────────────┐
│                  State Management                    │
│              (React Context + useReducer)            │
└───────────────────────┬─────────────────────────────┘
                        │ Actions
┌───────────────────────▼─────────────────────────────┐
│                  Service Layer                       │
│                                                      │
│  ┌────────────┐  ┌────────────┐  ┌──────────────┐   │
│  │ BLE Service │  │ Decoder   │  │ Export       │   │
│  └────────────┘  │ Service   │  │ Service      │   │
│                  └────────────┘  └──────────────┘   │
│  ┌────────────┐  ┌────────────┐  ┌──────────────┐   │
│  │ Threat     │  │ Integrity  │  │ Predictive   │   │
│  │ Detection  │  │ Verification│ │ Maintenance  │   │
│  └────────────┘  └────────────┘  └──────────────┘   │
│  ┌────────────┐  ┌────────────┐                      │
│  │ CAN        │  │ Attack     │                      │
│  │ Firewall   │  │ Simulator  │                      │
│  └────────────┘  └────────────┘                      │
└───────────────────────┬─────────────────────────────┘
                        │ Data access
┌───────────────────────▼─────────────────────────────┐
│                  Data Layer                          │
│  ┌────────────┐  ┌────────────┐  ┌──────────────┐   │
│  │ SQLite DB  │  │ Config    │  │ File Storage │   │
│  │            │  │ Files     │  │ (Exports)    │   │
│  └────────────┘  └────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────┘
```

## Layer Descriptions

### UI Layer

React components organised by feature domain:

- **Dashboard** — Real-time signal display, CAN traffic visualisation
- **Alerts** — Alert history, severity filter, detail view
- **Configuration** — Vehicle profile, firewall rules, maintenance thresholds
- **Maintenance** — Trend charts, prediction timeline, maintenance log
- **Security** — ECU fingerprints, integrity snapshots, attack simulation
- **Settings** — App preferences, data management, key management

All components are functional components using React hooks. No class components.

### State Management

React Context with useReducer for global state. Domain-specific contexts:

- `VehicleContext` — Connected vehicle state, decoded signals
- `AlertContext` — Active and historical alerts
- `ConfigContext` — User configuration and preferences
- `AuthContext` — Authentication state and key material
- `SessionContext` — Gateway connection state

### Service Layer

Each service is a singleton module exposing async functions:

| Service | Responsibility |
|---------|---------------|
| BLEService | Gateway connection, frame streaming, command interface |
| DecoderService | OpenDBC loading, frame decoding, signal normalisation |
| ThreatDetectionService | Rule matching, anomaly scoring, alert generation |
| IntegrityService | ECU fingerprinting, baseline management, comparison |
| PredictiveMaintenanceService | Signal trend analysis, prediction generation |
| CANFirewallService | Rule evaluation, match logging, alert dispatch |
| AttackSimulatorService | Scenario loading, CAN message injection simulation |
| ExportService | CSV/JSON export, report generation |
| ConfigService | Configuration file loading, validation, storage |

### Data Layer

- **SQLite** — Primary storage for decoded signals, alerts, fingerprints, maintenance history, session logs
- **Configuration Files** — JSON files for firewall rules, attack signatures, maintenance rules, vehicle profiles
- **File Storage** — Export files, crash reports (opt-in), baseline snapshots

## Decoder Adapter Layer

This is the critical boundary between SecureCAN and OpenDBC.

```
┌──────────────────────────────────────────────┐
│           Decoder Adapter Layer                │
│                                                │
│  ┌─────────────────────────────────────────┐   │
│  │      BaseDecoder (abstract)              │   │
│  │  + loadDBC(path): void                   │   │
│  │  + decodeFrame(frame): DecodedSignal[]   │   │
│  │  + getSignal(name): SignalDef            │   │
│  │  + getSignals(): SignalDef[]             │   │
│  └──────────────┬──────────────────────────┘   │
│                  │                              │
│  ┌───────────────┼───────────────────────┐     │
│  │               │                       │     │
│  ▼               ▼                       ▼     │
│  ┌──────┐  ┌──────────┐  ┌──────────────────┐ │
│  │ Honda│  │ Toyota   │  │ VehicleAdapter   │ │
│  │Adapter│ │ Adapter  │  │ (generic fallback)│ │
│  └──────┘  └──────────┘  └──────────────────┘ │
└────────────────────────────────────────────────┘
```

The base decoder loads OpenDBC parser output and converts it to SecureCAN's internal signal model. Vehicle adapters handle make-specific signal naming conventions and scaling factors. The generic fallback adapter provides basic decoding for vehicles without a specific adapter.

## Error Handling

- All service functions return `Result<T, Error>` discriminated union types
- UI layer displays user-friendly error messages from error codes
- Critical errors (authentication failure, database corruption) trigger specific alert flows
- Non-critical errors (transient BLE disconnection) trigger automatic retry with exponential backoff

## Threading Model

- JavaScript thread handles UI rendering and state management
- Service layer operations run on async background threads
- Decoder Adapter Layer uses native modules for CPU-intensive decoding
- Database operations use a dedicated SQLite queue

---

**TODOs**

- [ ] Define complete TypeScript interface for BaseDecoder
- [ ] Implement Result<T, Error> utility type
- [ ] Specify native module interfaces for iOS and Android
- [ ] Document service initialisation and shutdown sequence
