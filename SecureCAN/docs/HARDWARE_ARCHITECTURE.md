# Hardware Architecture — SecureCAN Gateway

## Purpose

Define the hardware design, component selection, electrical specifications, and PCB layout requirements for the SecureCAN Gateway.

## Scope

This document covers the ESP32-S3 based gateway hardware, including CAN interface, power regulation, radio subsystems, and mechanical enclosure. It is intended for firmware developers, electrical engineers, and hardware reviewers.

## Hardware Block Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                   SecureCAN Gateway v1                        │
│                                                              │
│  ┌──────────────────────┐   ┌──────────────────────────┐    │
│  │   OBD-II Connector    │   │   USB-C (Debug/Power)    │    │
│  │   (SAE J1962)         │   │                          │    │
│  └────────┬─────────────┘   └──────────┬───────────────┘    │
│           │                             │                    │
│  ┌────────▼─────────────┐   ┌──────────▼───────────────┐    │
│  │   12V→5V Regulator   │   │   5V→3.3V Regulator      │    │
│  │   (LM2596-based)     │   │   (AMS1117-3.3)           │    │
│  └────────┬─────────────┘   └──────────┬───────────────┘    │
│           │                             │                    │
│  ┌────────▼─────────────────────────────▼───────────────┐    │
│  │                   ESP32-S3 Module                      │    │
│  │  ┌──────────────────────────────────────────────┐     │    │
│  │  │  Xtensa LX7 Dual-Core @ 240 MHz               │     │    │
│  │  │  512 KB SRAM / 16 MB Flash                    │     │    │
│  │  ├──────────────────────────────────────────────┤     │    │
│  │  │  BLE 5.0 / Wi-Fi 802.11 b/g/n                │     │    │
│  │  ├──────────────────────────────────────────────┤     │    │
│  │  │  TWAI Controller (CAN 2.0)                   │     │    │
│  │  ├──────────────────────────────────────────────┤     │    │
│  │  │  GPIO: CAN Transceiver CS, Status LEDs,      │     │    │
│  │  │         Write-Enable Switch, Boot Button      │     │    │
│  │  └──────────────────────────────────────────────┘     │    │
│  └────────┬──────────────────────────────────────────────┘    │
│           │                                                    │
│  ┌────────▼─────────────┐   ┌──────────────────────────┐    │
│  │  CAN Transceiver     │   │  Status LEDs              │    │
│  │  (SN65HVD230)        │   │  • Power (Green)          │    │
│  │  3.3V, 1 Mbps        │   │  • CAN Activity (Yellow)  │    │
│  └────────┬─────────────┘   │  • Alert (Red)            │    │
│           │                 │  • BLE Connected (Blue)   │    │
│  ┌────────▼─────────────┐   └──────────────────────────┘    │
│  │  CAN Bus Terminator  │                                    │
│  │  (120 Ω, switchable) │   ┌──────────────────────────┐    │
│  └──────────────────────┘   │  Write-Enable Switch      │    │
│                              │  (Hardware DIP switch,   │    │
│                              │  MVP: always disabled)   │    │
│                              └──────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Component Specifications

### ESP32-S3 Module

| Parameter | Specification |
|-----------|--------------|
| MCU | Xtensa LX7 dual-core |
| Clock Speed | Up to 240 MHz |
| SRAM | 512 KB |
| Flash | 16 MB (Quad SPI) |
| BLE | 5.0 LE with Secure Connections |
| Wi-Fi | 802.11 b/g/n, 2.4 GHz |
| TWAI | Built-in CAN 2.0 controller |
| GPIO | 20 available pins |
| Operating Temp | -40°C to +85°C |

### CAN Transceiver — SN65HVD230

| Parameter | Specification |
|-----------|--------------|
| Protocol | CAN 2.0A, CAN 2.0B |
| Data Rate | Up to 1 Mbps |
| Supply Voltage | 3.0V to 3.6V |
| Bus Voltage | -2V to +7V common mode |
| Standby Mode | Available (low power) |
| Thermal Shutdown | Yes |
| Operating Temp | -40°C to +125°C |

### Power Regulation

| Stage | Regulator | Input | Output | Max Current |
|-------|-----------|-------|--------|-------------|
| OBD-II 12V→5V | LM2596 | 8V–40V | 5.0V | 3A |
| 5V→3.3V | AMS1117-3.3 | 5.0V | 3.3V | 1A |

### OBD-II Connector Pin Mapping (SAE J1962)

| Pin | Signal | Connection |
|-----|--------|------------|
| 4 | Chassis Ground | Ground plane |
| 5 | Signal Ground | Ground plane |
| 6 | CAN High (ISO 15765-4) | SN65HVD230 CANH |
| 14 | CAN Low (ISO 15765-4) | SN65HVD230 CANL |
| 16 | Battery Power (12V) | LM2596 input |

## Mechanical Specifications

| Parameter | Specification |
|-----------|--------------|
| PCB Dimensions | 60 mm × 40 mm × 1.6 mm |
| Layer Count | 4-layer stackup |
| Enclosure | 3D-printed ABS or injection-moulded polycarbonate |
| Enclosure Dimensions | 70 mm × 50 mm × 25 mm |
| Weight | < 50 g |
| Mounting | OBD-II pass-through (male/female connector) |

## Electrical Ratings

| Parameter | Min | Typical | Max | Unit |
|-----------|-----|---------|-----|------|
| Supply Voltage | 8 | 12 | 16 | V |
| Supply Current (active) | — | 200 | 350 | mA |
| Supply Current (standby) | — | 50 | 80 | mA |
| CAN Bus Voltage (differential) | — | 2.0 | — | V |
| Isolation | — | — | — | None (non-isolated MVP) |

## Environmental Ratings

| Parameter | Specification |
|-----------|--------------|
| Operating Temperature | -20°C to +70°C |
| Storage Temperature | -40°C to +85°C |
| Ingress Protection | IP40 (vented enclosure) |
| Vibration Resistance | SAE J1455 compliant |

## Bill of Materials (Preliminary)

| Component | Part Number | Quantity | Estimated Cost |
|-----------|-------------|----------|----------------|
| MCU Module | ESP32-S3-DevKitC-1 | 1 | $8.00 |
| CAN Transceiver | SN65HVD230DR | 1 | $1.50 |
| 12V→5V Regulator | LM2596 Module | 1 | $2.00 |
| 3.3V Regulator | AMS1117-3.3 | 1 | $0.50 |
| CAN Termination | 120Ω resistor | 1 | $0.10 |
| DIP Switch | 1-pole SPDT | 1 | $0.30 |
| LEDs | 0805 SMD (4 pcs) | 4 | $0.20 |
| Resistors/Caps | Various 0603 | 15 | $0.50 |
| PCB | 4-layer 60×40mm | 1 | $2.00 |
| Enclosure | 3D-printed ABS | 1 | $1.50 |
| Connector | OBD-II male | 1 | $1.00 |
| Connector | OBD-II female | 1 | $1.00 |
| **Total BOM Cost** | | | **~$18.60** |

## Design Notes

1. The MVP gateway uses non-isolated CAN transceiver. Future revisions shall include galvanic isolation (ISO1042 or similar) for production safety.
2. The write-enable DIP switch is a hardware-only safety mechanism. When disabled, the TWAI controller is placed in listen-only mode at the hardware level, making CAN transmission physically impossible.
3. A 120-ohm termination resistor is switchable via a solder jumper. Most OBD-II implementations include termination; the jumper prevents double-termination.
4. The ESP32-S3's built-in TWAI controller supports CAN 2.0 only. CAN FD requires an external controller (MCP2517FD or similar) and is deferred to Phase 5.

---

**TODOs**

- [ ] Produce full schematic and PCB layout files (KiCad)
- [ ] Evaluate galvanic isolation options (ISO1042, ADM3053)
- [ ] Conduct thermal analysis at 70°C ambient
- [ ] Design OBD-II pass-through mechanical enclosure
- [ ] Specify production test points and JTAG interface
- [ ] Define EMC/EMI compliance testing plan (CISPR 25)
