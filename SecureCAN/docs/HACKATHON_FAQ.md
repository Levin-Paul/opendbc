# Hackathon FAQ — SecureCAN

## Purpose

Provide quick-start information for developers contributing to SecureCAN during hackathons, open-source sprints, or first-time contributions.

## Quick Start

### Prerequisites

| Requirement | Version | Check |
|-------------|---------|-------|
| Node.js | ≥ 18 LTS | `node --version` |
| npm | ≥ 9 | `npm --version` |
| Python | ≥ 3.10 | `python --version` |
| ESP-IDF | ≥ 5.0 | `idf.py --version` |
| Git | ≥ 2.30 | `git --version` |

### Clone and Build

```bash
git clone --recursive https://github.com/securecan/securecan.git
cd securecan

# Install app dependencies
cd src && npm install && cd ..

# Build gateway firmware
cd firmware/esp32 && idf.py build && cd ../..
```

## Project Structure

```
SecureCAN/
├── src/              # React Native mobile app
│   ├── services/     # Service layer (BLE, decoder, detection, etc.)
│   ├── components/   # UI components
│   ├── screens/      # Screen components
│   ├── db/           # Database schema and migrations
│   └── __tests__/    # Jest tests
├── firmware/         # ESP32 gateway firmware
│   └── esp32/        # ESP-IDF project
├── docs/             # Documentation
├── configs/          # Configuration files
├── prompts/          # AI development prompts
├── memory/           # Sprint tracking
├── opendbc/          # OpenDBC submodule (read-only!)
└── tools/            # Build and utility scripts
```

## Important Rules

### 1. Never Modify OpenDBC

The `opendbc/` directory is a read-only git submodule. You must not:

- Edit any file inside `opendbc/`
- Add custom DBC definitions there
- Reference unmerged OpenDBC changes

Instead, use the Decoder Adapter Layer in `src/services/decoder/`.

### 2. Follow the Product Constitution

See `PRODUCT_CONSTITUTION.md`. Key rules:

- Offline-first: no required cloud dependencies
- Privacy-first: no data collection without consent
- Read-only MVP: no CAN write capability
- User-owned keys: keys generated on device
- Explainable alerts: every alert must be human-readable

### 3. Use TypeScript Strict Mode

All app code must compile with `strict: true` in tsconfig. No `any` types.

## Good First Issues

| Area | Difficulty | Description |
|------|------------|-------------|
| Decoder Adapter | Beginner | Add vehicle adapter for a make supported by OpenDBC |
| Alert UI | Beginner | Build alert detail screen with severity badge |
| Firewall Rules | Intermediate | Add new firewall rule category |
| Trend Analysis | Intermediate | Implement moving average trend method |
| BLE Protocol | Intermediate | Add new message type for gateway status |
| Attack Scenario | Intermediate | Write new attack simulation scenario |
| ECU Fingerprinting | Advanced | Improve fingerprint matching algorithm |
| CAN Bus Statistics | Advanced | Build bus utilisation dashboard component |

## Where to Get Help

| Resource | Location |
|----------|----------|
| Documentation | `docs/` directory |
| Issue Tracker | GitHub Issues |
| Internal Prompts | `prompts/` directory (AI-assisted dev) |
| Sprint Tracking | `memory/` directory |
| Architecture Decisions | `memory/DECISIONS.md` |

## Testing Your Changes

```bash
# Run app unit tests
cd src && npm test

# Run specific test
cd src && npx jest services/decoder

# Build and test firmware
cd firmware/esp32 && idf.py build && idf.py test
```

## Common Pitfalls

1. **Forgetting the OpenDBC boundary** — Double-check imports; never import directly from `opendbc/` source. Use the Decoder Adapter Layer.

2. **Adding cloud dependencies** — If your code needs internet access, it must be optional and gracefully degraded. No hard cloud dependencies.

3. **Storing keys in SQLite** — Authentication keys must use iOS Keychain or Android Keystore. Never store private keys in the database.

4. **Skipping alert explanations** — Every new detection rule must include a human-readable alert template with context and recommended action.

5. **Not writing tests** — All new services must have at least unit test coverage. No exceptions.

## Hackathon Project Ideas

1. **New Vehicle Adapter** — Add support for a vehicle make not yet covered. Use the Decoder Adapter Layer interface.
2. **Custom Attack Simulator** — Build a new attack scenario: UDS diagnostic injection, odometer tampering, or airbag control override simulation.
3. **Maintenance Dashboard** — Build a dedicated maintenance view with trend charts, prediction timelines, and service interval calendar.
4. **CAN Bus Topology Mapper** — Automatically map the CAN bus topology: discover all ECUs, message relationships, and bus hierarchy.
5. **Data Exporter** — Export alerts and maintenance data to industry-standard formats (AutoCare, Mitchell 1).
6. **Multi-Bus Support** — Extend the gateway and app to support vehicles with multiple CAN buses (CAN0, CAN1, etc.).
7. **Voice Alerts** — Integrate text-to-speech for critical alerts during driving (accessibility feature).

---

**TODOs**

- [ ] Add more good-first-issue tags to GitHub Issues
- [ ] Create hackathon starter templates
- [ ] Write vehicle adapter tutorial in docs
- [ ] Set up hackathon judging criteria and prizes
