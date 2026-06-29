# Virtual Vehicle Security Demo

Demonstrates the product **without a real car**: Python backend, fake CAN bus, authentication, and CAN firewall logic modeled on [opendbc safety](https://github.com/commaai/opendbc/tree/master/opendbc/safety).

## Quick start

```bash
cd opendbc
pip install -e ".[dashboard]"
python -m opendbc.simulation.server   # API :8080

# separate terminal
cd dashboard && npm install && npm run dev   # UI :5173
```

CLI-only demo:

```bash
python -m opendbc.simulation.demo
```

## Architecture

```
  Client (authorized app)
        │  ECDSA sign nonce
        ▼
  SecurityGateway  ──►  AuthEngine (challenge + session token)
        │  CAN firewall (block steer/brake/gas without controls_allowed)
        ▼
  CANBus (in-process)
        │
        ▼
  FakeVehicleSimulator  (RPM, speed, doors, ignition, ECUs)
```

## Modules

| Module | Role |
|--------|------|
| `opendbc/simulation/auth.py` | P-256 ECDSA challenge-response, HMAC session tokens, replay IDs |
| `opendbc/simulation/can_bus.py` | Fake CAN publish/subscribe |
| `opendbc/simulation/vehicle.py` | Simulated powertrain / body / ECU heartbeat frames |
| `opendbc/simulation/gateway.py` | Virtual ESP32: verify auth, forward safe TX, block dangerous TX |
| `opendbc/simulation/threats.py` | Unauthorized access, replay, injection scenarios |
| `opendbc/simulation/demo.py` | End-to-end scripted prototype |

## CAN IDs (demo protocol)

| ID | Type | Notes |
|----|------|-------|
| `0x100–0x102` | Read | Vehicle state, doors, ECU heartbeat |
| `0x210` | Safe write | Door lock (requires session) |
| `0x200–0x202` | Dangerous | Steer / brake / gas (session + `controls_allowed`) |

This mirrors opendbc’s safety model: buses stay silent until a safety mode allows output; actuation requires `controls_allowed`.

## Extending

- Wire `opendbc.can.CANPacker` to a real DBC for brand-specific IDs.
- Replace `CANBus` with socketcan or panda when hardware is available.
- Flash real ESP32 firmware that implements the same challenge/session checks.
