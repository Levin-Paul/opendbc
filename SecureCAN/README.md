# SecureCAN

Offline-first automotive cybersecurity, vehicle integrity verification, and predictive maintenance platform.

SecureCAN provides real-time CAN bus monitoring, threat detection, ECU integrity verification, sensor validation, and predictive maintenance — all operating offline by default with no mandatory cloud dependency.

## Quick Start

```bash
# Clone with submodules
git clone --recursive https://github.com/securecan/securecan.git

# Install dependencies
cd securecan
npm install

# Build gateway firmware
cd firmware/esp32
idf.py build
```

## Architecture Overview

```
React Native App
|
├── Notification Engine
├── Threat Detection → Integrity Verification → Predictive Maintenance
├── Decoder Adapter Layer (OpenDBC)
└── Wi-Fi Client (bulk CAN) ──┐
    BLE Client (auth/alerts) ──┤
                               │
       ┌───────────────────────┘
       ▼
ESP32 SecureCAN Gateway
|
├── Authentication Engine → Session Manager
├── CAN Monitor → Frame Buffer
└── TWAI Controller
       |
Vehicle CAN Network
```

## Key Features

- **Authentication** — Mutual challenge-response protocol with user-owned cryptographic keys
- **CAN Monitoring** — Real-time packet capture and decoding via OpenDBC
- **CAN Firewall** — Rule-based allow/block/drop filter engine
- **ECU Verification** — Fingerprint and response-based ECU identity checks
- **Sensor Verification** — Plausibility and calibration validation
- **Predictive Maintenance** — Signal trend analysis and wear forecasting
- **Threat Detection** — Anomaly detection against known attack signatures and baselines
- **Attack Simulation** — Offline replay and injection simulation engine
- **Offline-First** — No mandatory cloud connectivity; all processing local

## Repository Structure

```
SecureCAN/
├── README.md
├── PRODUCT.md
├── VISION.md
├── PROJECT_CONTEXT.md
├── PRODUCT_CONSTITUTION.md
├── ROADMAP.md
├── CHANGELOG.md
├── docs/          # Comprehensive documentation
├── configs/       # Configuration files and rule sets
├── prompts/       # AI-assisted development prompts
├── memory/        # Sprint and decision tracking
├── src/           # Application source code
├── firmware/      # ESP32 gateway firmware
└── opendbc/       # OpenDBC submodule (external, read-only)
```

## OpenDBC Integration

SecureCAN consumes the [OpenDBC](https://github.com/commaai/opendbc) repository as an external CAN decoding dependency. All DBC definitions are read-only. Vehicle-specific adapters wrap OpenDBC parsers to normalize signal output. No DBC files or OpenDBC source files are modified by SecureCAN.

## Security Principles

- Offline-first architecture
- Privacy-first data handling
- User-owned cryptographic keys
- No mandatory cloud dependency
- Read-only MVP (no CAN writes); attack simulation is software-only
- Fail-safe design
- Transparent and explainable alerts

## License

Proprietary. See LICENSE file for details.

---

**TODOs**

- [ ] Complete MVP implementation of CAN monitoring dashboard
- [ ] Finalize ESP32 BLE/Wi-Fi gateway firmware
- [ ] Implement vehicle adapter for top 5 vehicle makes
- [ ] Build attack simulation test harness
- [ ] Write integration tests for OpenDBC decoder wrappers
