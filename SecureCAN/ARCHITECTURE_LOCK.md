# SecureCAN Architecture Lock

## Purpose

This document is the permanent architectural reference for SecureCAN.

It defines the system that every future implementation must follow.

No AI agent or developer may redesign SecureCAN without explicitly updating this document.

---

# Product Vision

SecureCAN is an offline-first automotive cybersecurity platform that protects vehicle networks, verifies component integrity, and provides predictive maintenance while preserving complete user ownership of vehicle data.

---

# Core Principles

- Offline First
- Privacy First
- User-Owned Cryptographic Keys
- Read-Only MVP
- No Cloud Requirement
- Transparent Security
- Explainable Alerts
- Modular Architecture

---

# OpenDBC

OpenDBC is the official CAN decoding engine.

Rules:

- Never modify OpenDBC.
- Treat OpenDBC as an external dependency.
- Build wrappers and adapters only.
- Never duplicate DBC definitions.
- Pin OpenDBC to a specific Git commit.

---

# Software Architecture

Mobile Application

↓

BLE / Wi-Fi

↓

ESP32 SecureCAN Gateway

↓

Authentication

↓

Session Manager

↓

CAN Monitor

↓

OpenDBC Adapter

↓

Signal Service

↓

Threat Detection

↓

Integrity Verification

↓

Maintenance Engine

↓

Notification Engine

↓

Vehicle CAN Network

---

# Hardware Architecture

ESP32-S3

↓

TWAI Controller

↓

OBD-II Connector

↓

Vehicle CAN Bus

↓

Vehicle ECUs

---

# Authentication

Mutual authentication.

Gateway verifies App.

App verifies Gateway.

Encrypted session established.

---

# Transport

BLE

Used for:

- Authentication
- Alerts
- Vehicle Status
- Health Data

Wi-Fi

Used for:

- Firmware Updates
- Diagnostics
- High-Speed CAN Capture
- Developer Mode

---

# OpenDBC Layer

Responsibilities

- Decode CAN frames
- Load vehicle profiles
- Parse signals

SecureCAN Responsibilities

- Threat Detection
- Integrity Verification
- Predictive Maintenance
- Notifications
- User Interface

---

# Read-Only Policy

MVP and Version 1.0 are read-only.

The system shall never:

- Flash ECUs
- Modify vehicle configuration
- Send unsafe CAN messages

Research features may be developed separately and are not part of the production application.

---

# Future AI Instructions

Every future coding session shall:

1. Read PRODUCT_CONSTITUTION.md
2. Read PROJECT_CONTEXT.md
3. Read ARCHITECTURE_LOCK.md
4. Read IMPLEMENTATION_ORDER.md
5. Read all JSON configuration files

Implementation must follow these documents.

If a request conflicts with this architecture:

Do not change the architecture.

Explain the conflict.

Request confirmation before making architectural changes.

---

# Final Rule

Architecture stability is more important than implementation speed.

Consistency is more important than adding features.