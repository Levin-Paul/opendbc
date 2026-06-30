# Trust Model — SecureCAN

## Purpose

Define the trust relationships, trust boundaries, and trust assumptions across all SecureCAN system components.

## Scope

This document covers the trust model between the user, the mobile app, the gateway, and the vehicle. It defines who or what is trusted, for which operations, and under what conditions.

## Trust Boundaries

```
┌─────────────────────────────────────────────────────┐
│                  User Domain                         │
│  (Trusted — full control)                            │
│  • Mobile device                                       │
│  • User-generated cryptographic keys                   │
│  • Configuration choices                               │
│  • Data export decisions                               │
└────────────────────┬────────────────────────────────┘
                     │
          Trust Boundary 1 (BLE/Wi-Fi)
          Encrypted channel, authenticated
                     │
┌────────────────────▼────────────────────────────────┐
│              SecureCAN Gateway                       │
│  (Trusted for monitoring — NOT trusted for writes)    │
│  • CAN frame capture and forwarding                   │
│  • Authentication enforcement                         │
│  • Firmware integrity                                 │
│  • Hardware write-enable mechanism                    │
└────────────────────┬────────────────────────────────┘
                     │
          Trust Boundary 2 (CAN Bus)
          Untrusted — messages can be spoofed
                     │
┌────────────────────▼────────────────────────────────┐
│              Vehicle CAN Network                      │
│  (Untrusted — no inherent authentication)             │
│  • Multiple ECUs communicating without auth           │
│  • Any physically connected device can inject         │
│  • No message origin verification                     │
└─────────────────────────────────────────────────────┘
```

## Trust Assumptions

### TA-01 — User Device
The user's mobile device is trusted. It is the root of trust for cryptographic key generation and storage. If the mobile device is compromised, all SecureCAN security guarantees are invalid.

### TA-02 — Gateway Hardware
The SecureCAN Gateway hardware is trusted for read operations. The hardware write-enable switch provides a physical guarantee that the gateway cannot transmit CAN messages when disabled. The gateway is NOT trusted when write capability is enabled.

### TA-03 — Gateway Firmware
Gateway firmware is trusted after signature verification during update. The initial firmware is flashed via USB-C with physical access required. All subsequent updates require Ed25519 signatures verified by a public key embedded in the bootloader.

### TA-04 — CAN Bus
The CAN bus is untrusted. Any message on the bus may be spoofed, replayed, or injected by any device physically connected to the bus. SecureCAN operates under the assumption that the bus is a hostile network.

### TA-05 — OpenDBC
OpenDBC signal definitions are trusted for signal decoding accuracy but not for completeness. DBC files may contain errors or omissions. The Decoder Adapter Layer validates signal ranges independently.

### TA-06 — Communication Channel
BLE/Wi-Fi communication is encrypted and authenticated. The channel is trusted after the challenge-response handshake completes successfully. Unauthenticated connections receive basic monitoring data but cannot modify configuration.

### TA-07 — Third-Party Libraries
Third-party dependencies (React Native, BLE libraries, SQLite) are trusted for correct operation but not for security. All security-sensitive operations use platform-native cryptographic APIs rather than library-provided crypto.

## Trust Levels

| Component | Trust Level | Rationale |
|-----------|-------------|-----------|
| User mobile device | Full | Root of trust for keys and decisions |
| User's cryptographic keys | Full | Generated on-device, never shared |
| SecureCAN Gateway (read-only) | High | Hardware-enforced read-only mode |
| SecureCAN Gateway (write-enabled) | Low | Capable of bus injection |
| OpenDBC definitions | Medium | Community-maintained, potential inaccuracies |
| CAN bus messages | None | No inherent authentication |
| Third-party libraries | Medium | Subject to vulnerabilities |
| Cloud services (if used) | None by default | User must explicitly opt in |

## Trust Decision Matrix

| Operation | Requires Authentication | Requires Write-Enable | Trust Level Required |
|-----------|------------------------|----------------------|---------------------|
| View CAN traffic | No | No | Low |
| View decoded signals | No | No | Low |
| View alerts | No | No | Low |
| Change firewall rules | Yes | No | High |
| Change maintenance thresholds | Yes | No | High |
| Enable CAN write capability | Yes | Yes (hardware + software) | Full |
| Update gateway firmware | Yes | Yes (physical access) | High |
| Export data | Yes | No | Medium |
| Delete data | Yes | No | High |
| Enable cloud features | Yes | No | User decision |

---

**TODOs**

- [ ] Review trust assumptions with security audit team
- [ ] Define incident response plan for trust boundary violations
- [ ] Document key rotation and revocation procedures
- [ ] Specify hardware security module (HSM) integration for Phase 4
