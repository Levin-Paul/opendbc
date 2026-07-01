# SecureCAN Implementation Order

## Purpose

This document defines the official implementation sequence for SecureCAN.

The order described here is mandatory.

Future development shall follow this order unless an architectural review explicitly changes it.

---

# Phase 0 — Foundation

## Objectives

- Verify project architecture
- Verify OpenDBC integration
- Prepare development environment

### Tasks

- [ ] Clone OpenDBC as a Git submodule
- [ ] Verify OpenDBC builds correctly
- [ ] Verify supported vehicle profiles
- [ ] Build OpenDBC Adapter Layer
- [ ] Build Signal Abstraction Layer

Deliverable:

A normalized signal interface independent of OpenDBC internals.

---

# Phase 1 — Backend

## Objectives

Create the SecureCAN backend.

### Components

- Authentication Service
- Session Manager
- Vehicle Manager
- Alert Manager
- Notification Service
- Health Service

Deliverable:

REST API with authentication.

---

# Phase 2 — Firmware

## Objectives

Develop ESP32 firmware.

### Components

- BLE
- Wi-Fi
- TWAI Driver
- Cryptography
- Secure Storage
- OTA

Deliverable:

Gateway firmware capable of secure communication.

---

# Phase 3 — Simulation

## Objectives

Develop a complete virtual vehicle.

### Components

- CAN Frame Generator
- Vehicle Profiles
- Attack Simulator
- Threat Engine
- Maintenance Simulator

Deliverable:

Offline testing without a real vehicle.

---

# Phase 4 — Mobile Application

## Objectives

Develop the mobile application.

### Screens

- Login
- Dashboard
- Vehicle Status
- Health
- Alerts
- Attack Simulator
- Settings

Deliverable:

Complete MVP application.

---

# Phase 5 — Integration

## Objectives

Connect every subsystem.

### Integrations

- Firmware ↔ Backend
- Backend ↔ OpenDBC
- Backend ↔ Mobile App
- Simulator ↔ Backend

Deliverable:

Complete software stack.

---

# Phase 6 — Hardware

## Objectives

Bring the software onto physical hardware.

### Hardware

- ESP32-S3
- OBD-II Connector
- TWAI Interface
- Secure Storage
- Sensors

Deliverable:

Working SecureCAN prototype.

---

# Phase 7 — Testing

## Objectives

Validate the entire system.

### Tests

- Unit Tests
- Integration Tests
- Hardware Tests
- Security Tests
- Vehicle Tests

Deliverable:

Stable MVP ready for demonstration.

---

# Rules

No future implementation may skip phases.

No feature shall be implemented before its dependencies are complete.

Architecture changes require updating ARCHITECTURE_LOCK.md before implementation.