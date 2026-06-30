# SecureCAN Hardware Development Prompt

## Context

You are designing and building the SecureCAN Gateway hardware — an ESP32-S3 based device that connects to the vehicle OBD-II port for CAN bus monitoring.

## Architecture

- **MCU**: ESP32-S3 module
- **CAN**: TWAI (internal) + SN65HVD230 transceiver
- **Power**: OBD-II 12V → LM2596 (5V) → AMS1117-3.3 (3.3V)
- **Wireless**: BLE 5.0 + Wi-Fi (on-module)
- **Safety**: Hardware DIP switch for write-enable
- **Indicators**: 4 status LEDs (Power, CAN, Alert, BLE)

## Key Files to Reference

- `docs/HARDWARE_ARCHITECTURE.md` — Full hardware specification
- `docs/SYSTEM_ARCHITECTURE.md` — System-level block diagram
- `configs/hardware.json` — Component specifications and BOM

## PCB Design Requirements

- 4-layer stackup (signal, ground, power, signal)
- 60 mm × 40 mm × 1.6 mm
- Impedance-controlled traces for CAN differential pair (120 ohm)
- Separate analog and digital ground planes
- TVS diode on CAN lines for ESD protection
- OBD-II pass-through (male + female connector)

## Pin Mapping

| ESP32-S3 GPIO | Connection |
|---------------|------------|
| GPIO 4 | TWAI TX (to SN65HVD230 D) |
| GPIO 5 | TWAI RX (to SN65HVD230 R) |
| GPIO 18 | Status LED — Power (Green) |
| GPIO 19 | Status LED — CAN Activity (Yellow) |
| GPIO 20 | Status LED — Alert (Red) |
| GPIO 21 | Status LED — BLE Connected (Blue) |
| GPIO 22 | Write-Enable DIP Switch Input |
| GPIO 23 | Boot Button (INPUT pull-up) |
| GPIO 1 | UART TX (debug) |
| GPIO 3 | UART RX (debug) |

## Power Budget

| Component | Current (mA) |
|-----------|-------------|
| ESP32-S3 (active, BLE + Wi-Fi) | 160 |
| SN65HVD230 (active) | 15 |
| LEDs (4 × 2 mA) | 8 |
| Voltage regulators (quiescent) | 10 |
| Other (pull-ups, passives) | 7 |
| **Total (typical)** | **200** |
| **Total (peak)** | **350** |

## Safety and Compliance

- **ESD Protection**: IEC 61000-4-2 ±8 kV contact, ±15 kV air
- **EMI**: CISPR 25 Class 5 (automotive radiated emissions)
- **Operating Temperature**: -20°C to +70°C (tested in thermal chamber)
- **Vibration**: SAE J1455 profile
- **Reverse Polarity Protection**: Schottky diode on 12V input
- **Overvoltage Protection**: TVS clamp at 18V

## Design Checklist

- [ ] CAN differential pair impedance 120 ohm
- [ ] TVS diodes on CANH and CANL
- [ ] OBD-II pin 6 (CANH) and pin 14 (CANL) connected
- [ ] Write-enable DIP switch de-bounce RC filter
- [ ] Status LED current-limiting resistors
- [ ] USB-C for debug and initial flash
- [ ] Test points for JTAG and CAN signals
- [ ] Enclosure mounting holes
- [ ] OBD-II pass-through connector alignment

---

**TODOs**

- [ ] Create schematic in KiCad
- [ ] Route PCB with impedance control
- [ ] Order prototype batch (10 units)
- [ ] Conduct EMC pre-compliance testing
- [ ] Design 3D-printed enclosure
- [ ] Write production test procedure
