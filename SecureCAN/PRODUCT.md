# Product Overview — SecureCAN

**Version:** 0.1.0  
**Status:** Pre-alpha / MVP Development  
**Last Updated:** 2026-06-30

## Purpose

SecureCAN is an offline-first automotive cybersecurity platform purpose-built for vehicle owners, fleet operators, and aftermarket workshops who need real-time visibility into their vehicle's CAN bus activity, component integrity, and maintenance state without relying on cloud infrastructure or third-party telemetry services.

## Problem Statement

Modern vehicles contain 70+ ECUs communicating over CAN bus networks. Vehicle owners have no visibility into this traffic. Security vulnerabilities in CAN bus architecture remain unpatched for years. Predictive maintenance data is locked inside OEM diagnostics tools. Existing aftermarket solutions either require cloud subscriptions, upload vehicle data to third-party servers, or are limited to basic OBD-II scan tools.

## Solution

SecureCAN is a hardware-software platform that:

1. Connects to the vehicle OBD-II port via an ESP32-based SecureCAN Gateway
2. Decodes CAN traffic using OpenDBC signal definitions
3. Applies real-time threat detection against known attack patterns
4. Verifies ECU and sensor integrity through fingerprinting and plausibility checks
5. Predicts component wear and maintenance needs from CAN signal trends
6. Provides an intuitive mobile dashboard over BLE or Wi-Fi
7. Stores all data locally on the user's device — no cloud upload required

## Target Users

| User | Primary Use Case |
|------|------------------|
| Vehicle Owner | Personal vehicle security monitoring and maintenance alerts |
| Fleet Operator | Multi-vehicle fleet integrity dashboard and predictive maintenance |
| Workshop | Diagnostic verification and post-repair integrity checks |
| Security Researcher | CAN bus attack surface analysis and simulation |

## Core Capabilities

- **CAN Bus Monitoring** — Real-time packet capture, filtering, and decoding
- **Threat Detection** — Injection, replay, spoofing, and bus-off attack detection
- **ECU Fingerprinting** — Identity verification against known ECU response profiles
- **Sensor Plausibility** — Cross-signal validation for speed, temperature, pressure, etc.
- **Predictive Maintenance** — Trend analysis on battery voltage, DPF pressure, brake wear, etc.
- **Integrity Verification** — Component-level integrity checks against baseline snapshots
- **Attack Simulation** — Offline "what-if" engine for evaluating attack scenarios
- **Secure Authentication** — Challenge-response handshake between app and gateway

## Non-Goals

- ECU flashing or reprogramming
- Vehicle tuning or performance modification
- GPS tracking or location logging
- Cloud data aggregation or telematics brokering
- ADAS system modification
- OEM diagnostic protocol reverse engineering beyond CAN decoding

---

**TODOs**

- [ ] Validate top-10 vehicle compatibility with OpenDBC coverage
- [ ] Define MVP feature freeze checklist
- [ ] Establish beta testing program for fleet operators
- [ ] Create product comparison matrix against existing tools
