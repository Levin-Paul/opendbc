# System Architecture — SecureCAN

## Purpose

Define the top-level system architecture of the SecureCAN platform, including hardware, software, communication protocols, and external dependencies.

## Scope

This document covers the complete system from the vehicle CAN bus through the SecureCAN Gateway, communication transport, and the mobile application. It does not cover internal software architecture of individual components.

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                  Vehicle CAN Network                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  ECU-1   │  │  ECU-2   │  │  ECU-3   │  │  ECU-n   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│         │             │             │             │         │
│         └─────────────┼─────────────┼─────────────┘         │
│                        │             │                      │
│              ┌─────────▼─────────────▼──────────┐           │
│              │        OBD-II (SAE J1962)         │           │
│              └─────────────────┬─────────────────┘           │
└────────────────────────────────┼──────────────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   SecureCAN Gateway      │
                    │     (ESP32-S3)           │
                    │                          │
                    │  ┌──────────────────┐    │
                    │  │ CAN Controller    │    │
                    │  │ (TWAI — built-in) │    │
                    │  └────────┬─────────┘    │
                    │           │              │
                    │  ┌────────▼─────────┐    │
                    │  │  Frame Buffer     │    │
                    │  │  (Ring Buffer)    │    │
                    │  └────────┬─────────┘    │
                    │           │              │
                    │  ┌────────▼─────────┐    │
                    │  │ Authentication   │    │
                    │  │ Engine           │    │
                    │  └────────┬─────────┘    │
                    │           │              │
                    │  ┌────────▼─────────┐    │
                    │  │ Session Manager   │    │
                    │  └────────┬─────────┘    │
                    │           │              │
                    │  ┌────────▼─────────┐    │
                    │  │ BLE/Wi-Fi Stack   │    │
                    │  └────────┬─────────┘    │
                    └───────────┼──────────────┘
                                │
              ┌─────────────────┼─────────────────┐
              │        BLE 5.0 / Wi-Fi            │
              │   (Encrypted — LE Secure Conn.)   │
              └─────────────────┬─────────────────┘
                                │
                    ┌───────────▼──────────────┐
                    │    SecureCAN Mobile App   │
                    │     (React Native)        │
                    │                           │
                    │  ┌───────────────────┐    │
                    │  │ BLE/Wi-Fi Client  │    │
                    │  └────────┬──────────┘    │
                    │           │               │
                    │  ┌────────▼──────────┐    │
                    │  │ Decoder Adapter   │    │
                    │  │ Layer (OpenDBC)   │    │
                    │  └────────┬──────────┘    │
                    │           │               │
                    │  ┌────────▼──────────┐    │
                    │  │ Threat Detection  │    │
                    │  │ Engine            │    │
                    │  └────────┬──────────┘    │
                    │           │               │
                    │  ┌────────▼──────────┐    │
                    │  │ Integrity Verif.  │    │
                    │  │ Engine            │    │
                    │  └────────┬──────────┘    │
                    │           │               │
                    │  ┌────────▼──────────┐    │
                    │  │ Predictive Maint. │    │
                    │  │ Engine            │    │
                    │  └────────┬──────────┘    │
                    │           │               │
                    │  ┌────────▼──────────┐    │
                    │  │ Notification      │    │
                    │  │ Engine            │    │
                    │  └────────┬──────────┘    │
                    │           │               │
                    │  ┌────────▼──────────┐    │
                    │  │ Local Database    │    │
                    │  │ (SQLite)          │    │
                    │  └───────────────────┘    │
                    └───────────────────────────┘
```

## Components

### 1. Vehicle CAN Network

The target CAN bus network as defined by ISO 11898. SecureCAN connects via the SAE J1962 OBD-II connector, pins 6 (CAN High) and 14 (CAN Low). The system passively listens to CAN traffic without transmitting.

### 2. SecureCAN Gateway

An ESP32-S3 microcontroller with:

- TWAI controller (built-in CAN 2.0 controller)
- BLE 5.0 radio for mobile app connectivity
- Wi-Fi radio for alternative transport
- Power from OBD-II port (12V to 5V/3.3V regulation onboard)
- Authentication engine performing Ed25519 challenge-response
- Session manager tracking authenticated client state
- Ring buffer for CAN frame temporary storage

### 3. Communication Transport

SecureCAN uses a dual-transport architecture:

- **BLE 5.0** — Used for authentication handshake, alert notifications, health status, and low-rate telemetry. All BLE communication uses LE Secure Connections encryption.
- **Wi-Fi (TCP)** — Used for bulk CAN frame capture, developer mode, high-speed diagnostics, and firmware updates.

The gateway supports both transports simultaneously. The protocol uses a compact binary frame format to minimise bandwidth on BLE.

### 4. SecureCAN Mobile App

React Native application running on iOS and Android. Subcomponents:

- **BLE/Wi-Fi Client** — Manages connection to gateway
- **Decoder Adapter Layer** — Loads OpenDBC definitions and decodes raw frames
- **Threat Detection Engine** — Analyses decoded signals against rules
- **Integrity Verification Engine** — ECU fingerprinting and baseline comparison
- **Predictive Maintenance Engine** — Trend analysis and alert generation
- **Notification Engine** — Alert routing and user notification
- **Local Database** — SQLite for all persistent storage

## Data Flow

1. CAN frames captured by gateway at OBD-II port
2. Frames timestamped and buffered in ring buffer
3. Bulk CAN frames streamed over Wi-Fi (TCP); alerts and health data transmitted over BLE
4. Decoder Adapter Layer decodes raw frames using OpenDBC
5. Decoded signals distributed to detection/verification/maintenance engines
6. Results stored in local SQLite database
7. Alerts dispatched through notification engine

## External Dependencies

| Dependency | Purpose | Integration Method |
|------------|---------|-------------------|
| OpenDBC | CAN signal definitions | Git submodule, read-only |
| ESP-IDF | ESP32 firmware SDK | V5.x framework |
| React Native | Mobile app framework | NPM package |
| react-native-ble-plx | BLE client library | NPM package |
| SQLite | Local database | react-native-sqlite-storage |

---

**TODOs**

- [ ] Produce detailed network topology diagram for multi-bus vehicles
- [ ] Specify BLE protocol binary frame format in API_SPEC.md
- [ ] Define gateway power management states (ignition on/off, sleep, active)
