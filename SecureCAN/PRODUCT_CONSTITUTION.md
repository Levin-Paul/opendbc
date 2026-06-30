# SecureCAN Product Constitution

This document defines the inviolable principles that govern all SecureCAN product decisions. No feature, design choice, or strategic pivot may violate these articles without a supermajority product council vote and constitutional amendment.

---

## Article I — Offline-First Mandate

**Section 1.** The platform must function fully and usefully without any internet connectivity. All core features — CAN monitoring, threat detection, integrity verification, predictive maintenance — must operate on local processing and local storage only.

**Section 2.** Cloud features may exist only as optional enhancements. A user who never connects to the internet must receive the same security and maintenance value as a user who enables cloud features.

**Section 3.** No telemetry, analytics, crash reporting, or usage data may be transmitted without explicit user consent provided through a separate opt-in mechanism.

## Article II — Privacy by Default

**Section 1.** All vehicle data — CAN signals, decoded values, diagnostic results, maintenance predictions — is stored exclusively on the user's device unless the user explicitly exports or shares it.

**Section 2.** The platform shall have no cloud data pipeline, no user account database, and no vehicle VIN lookup service that associates vehicle data with user identity.

**Section 3.** Cryptographic keys used for authentication and integrity verification are generated and stored on the user's device. SecureCAN infrastructure shall never possess or have access to user private keys.

## Article III — Read-Only Safety

**Section 1.** The MVP and v1.0 product shall be read-only. The SecureCAN Gateway may observe CAN traffic but shall never inject CAN messages onto the vehicle bus.

**Section 2.** Attack simulation is simulation-only during MVP and v1.0. The simulator replays or generates CAN frames within the mobile app's detection engine for testing purposes. No simulated frames are transmitted to the vehicle CAN bus. Live CAN injection is not permitted in MVP or v1.0.

**Section 3.** A hardware write-enable switch or software override that enables CAN write capability for future versions must require deliberate user action and display a clear safety warning. Write capability must default to disabled.

**Section 4.** Any future write-capable feature must undergo independent security audit and receive product council approval before implementation.

## Article IV — Transparency

**Section 1.** Every security alert must include a human-readable explanation of the detection, its potential impact, and recommended user action. Raw hex dumps alone are insufficient.

**Section 2.** The threat detection engine's logic must be documented and auditable. No proprietary black-box scoring algorithms.

**Section 3.** All attack signatures and detection rules shall be user-viewable and user-modifiable through configuration files.

## Article V — OpenDBC Boundary

**Section 1.** The OpenDBC repository is an upstream dependency consumed as a read-only submodule. No SecureCAN commit may modify any file within the opendbc directory tree.

**Section 2.** Vehicle support gaps in OpenDBC must be documented as product limitations, not worked around through custom DBC files within the SecureCAN repository.

**Section 3.** The Decoder Adapter Layer is the sole interface between SecureCAN and OpenDBC. No SecureCAN component outside this layer may directly reference OpenDBC types or parsers.

## Article VI — Fail-Safe Design

**Section 1.** Gateway firmware must implement a watchdog timer that resets the device if the main application thread hangs.

**Section 2.** Authentication failures between the mobile app and gateway must not block CAN monitoring. The gateway may restrict configuration changes when unauthenticated but must continue monitoring and alerting.

**Section 3.** Any firmware update that fails verification must be rejected, and the previous firmware must continue operating.

## Article VII — Explainable Alerts

**Section 1.** Alert severity levels are: INFO, WARNING, CRITICAL, and EMERGENCY. Each level has a defined response guideline.

**Section 2.** Every alert must contain: timestamp, affected component or signal, detection rule triggered, evidence summary, and recommended action.

---

**TODOs**

- [ ] Establish product council membership and voting procedures
- [ ] Create constitutional amendment process documentation
- [ ] Review constitution with legal counsel for regulatory compliance
