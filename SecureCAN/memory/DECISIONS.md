# Architecture Decisions Log

This file records significant architectural decisions made during SecureCAN development. Each entry follows the Architecture Decision Record (ADR) format.

---

## ADR-001 — Offline-First Architecture

**Status:** Accepted  
**Date:** 2026-06-30  
**Context:** The platform must function without internet connectivity. Cloud-first competitors exist but compromise privacy and reliability.  
**Decision:** All core features operate locally. Cloud features are optional add-ons. No telemetry without explicit opt-in.  
**Consequences:** No cloud revenue in MVP. Stronger privacy guarantees. Increased device storage requirements.  
**References:** PRODUCT_CONSTITUTION.md Article I

## ADR-002 — OpenDBC as Read-Only Submodule

**Status:** Accepted  
**Date:** 2026-06-30  
**Context:** CAN decoding requires DBC file definitions. OpenDBC provides 200+ vehicle definitions. Internal maintenance of DBC files is high-effort and low-value.  
**Decision:** Consume OpenDBC as a pinned git submodule. Never modify OpenDBC files. Build a Decoder Adapter Layer as the sole interface.  
**Consequences:** Vehicle coverage limited to OpenDBC's scope. Cannot fix DBC errors without upstream merge. Clean separation of concerns.  
**References:** PROJECT_CONTEXT.md, OPENDBC_INTEGRATION.md

## ADR-003 — Ed25519 for Mutual Authentication

**Status:** Accepted  
**Date:** 2026-06-30  
**Context:** Need asymmetric cryptographic authentication between app and gateway. Must work offline. Keys must be user-owned. Both parties must authenticate each other to prevent gateway impersonation and app impersonation.  
**Decision:** Use Ed25519 (RFC 8032) for mutual challenge-response authentication. The app requests a challenge from the gateway, signs the gateway's nonce, then the gateway signs its own nonce. Both parties verify the other's signature. Keys generated on-device. Private keys stored in platform keychain.  
**Consequences:** Strong mutual cryptographic identity. No shared secrets. Two round-trips required for full handshake. Key management requires user education.  
**References:** SECURITY_MODEL.md, API_SPEC.md, authentication.json

## ADR-004 — Read-Only MVP

**Status:** Accepted  
**Date:** 2026-06-30  
**Context:** CAN write capability is safety-critical. Premature write support increases attack surface and liability.  
**Decision:** MVP hardware includes write-enable DIP switch (default disabled). MVP firmware never initialises TWAI transmitter. MVP app never sends CAN frames.  
**Consequences:** Cannot test detection by injecting frames live (use simulation instead). Reduced attack surface. Stronger safety posture.  
**References:** PRODUCT_CONSTITUTION.md Article III

## ADR-005 — React Native for Mobile App

**Status:** Accepted  
**Date:** 2026-06-30  
**Context:** Need cross-platform mobile app (iOS + Android). Limited team resources. BLE library ecosystem required.  
**Decision:** Use React Native with TypeScript strict mode. react-native-ble-plx for BLE. Native modules for CPU-intensive decoder operations.  
**Consequences:** Single codebase for both platforms. BLE library fragmentation on Android. Decoder performance requires native module bridge.  
**References:** SOFTWARE_ARCHITECTURE.md

## ADR-006 — SQLite for Local Storage

**Status:** Accepted  
**Date:** 2026-06-30  
**Context:** Need offline-capable database for CAN frames, alerts, fingerprints, and maintenance data. Must support complex queries and time-series data.  
**Decision:** SQLite via react-native-sqlite-storage. WAL mode for concurrency. No encryption in MVP (SQLCipher planned for Phase 2).  
**Consequences:** Well-understood technology. Limited concurrent write performance. No built-in encryption.  
**References:** DATABASE.md

## ADR-007 — Dark Theme Only (MVP)

**Status:** Accepted  
**Date:** 2026-06-30  
**Context:** Automotive use requires low-glare display for night driving. Dark theme preferred for dashboards. Limited design resources.  
**Decision:** Dark theme is the default and only theme for MVP. High-contrast mode added for sunlight readability. Light theme deferred to Phase 2.  
**Consequences:** Faster theme implementation. Light theme users not supported in MVP. Reduced accessibility options.  
**References:** UI_GUIDELINES.md

---

**TODOs**

- [ ] Review ADR-001 through ADR-007 for continued validity at each phase
- [ ] Establish ADR review process (quarterly)
- [ ] Add ADR template to documentation guidelines
