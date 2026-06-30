# SecureCAN Vision

## Statement

Every vehicle owner should have the same level of visibility into their vehicle's electronic systems that they have into their home network. SecureCAN makes vehicle cybersecurity and maintenance transparency an accessible right, not a dealer-only privilege.

## The Problem We Exist To Solve

The CAN bus is the nervous system of every modern vehicle. It carries mission-critical signals — throttle position, brake pressure, steering angle, transmission state — across a network designed in the 1980s with no security provisions. There is no authentication, no encryption, no access control. Any device physically connected to the CAN bus can read every message and inject arbitrary traffic.

Despite this, vehicle owners have zero visibility into CAN bus activity. They cannot see which ECUs are communicating, whether a device has tampered with a sensor reading, or when a component is beginning to fail. The aftermarket diagnostics industry is dominated by cloud-dependent tools that treat vehicle data as a monetisable asset rather than the owner's private information.

## The Future We Build

A world where:

- Vehicle cybersecurity is as standard as home network security
- Predictive maintenance alerts come from on-device analysis, not cloud subscriptions
- Vehicle owners own their diagnostic data entirely
- Aftermarket workshops can verify repair integrity cryptographically
- Fleet operators have real-time integrity dashboards without uploading vehicle data
- Security researchers can simulate attacks to understand vehicle vulnerabilities safely

## Design North Stars

1. **Offline-First** — The platform must function fully without internet connectivity. Cloud features are optional additions, never requirements.

2. **Privacy by Default** — No vehicle data leaves the user's device unless the user explicitly exports it. No telemetry, no analytics pings, no background data collection.

3. **User-Owned Keys** — Authentication and integrity verification use cryptographic keys generated and stored on the user's device. SecureCAN has no access to user keys.

4. **Explainable Security** — Every alert must include a human-readable explanation of what was detected, why it matters, and what the user can do. No black-box threat scores.

5. **Fail-Safe** — The SecureCAN Gateway is a read-only monitoring device in its MVP configuration. It can observe and alert but cannot inject CAN traffic. Fail-safe is non-negotiable.

6. **OpenDBC Respect** — We consume OpenDBC as an upstream dependency. We never fork, patch, or maintain our own DBC definitions. Vehicle coverage gaps are documented, not duct-taped.

---

**TODOs**

- [ ] Formalise vision statement with advisory board review
- [ ] Publish public whitepaper on offline-first automotive security
- [ ] Define metrics for measuring vision alignment in product decisions
