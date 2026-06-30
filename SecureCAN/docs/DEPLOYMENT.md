# Deployment Guide — SecureCAN

## Purpose

Document the deployment process for all SecureCAN components: gateway firmware, mobile application, and configuration data.

## Scope

This guide covers development, staging, and production deployment for the SecureCAN Gateway (ESP32 firmware) and the SecureCAN Mobile App (React Native). Cloud deployment is not covered as the platform is offline-first.

## Architecture Overview

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Developer      │     │  Build Server   │     │  User Device    │
│  Workstation    │────→│  (GitHub CI)    │────→│  (Phone/Gateway)│
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Component Deployment

### 1. Gateway Firmware (ESP32)

#### Build

```bash
# Prerequisites: ESP-IDF v5.x
cd firmware/esp32
idf.py set-target esp32s3
idf.py build
```

Output: `firmware/esp32/build/securecan-gateway.bin`

#### Signing

```bash
# Firmware is signed with Ed25519
python tools/sign_firmware.py \
  --input build/securecan-gateway.bin \
  --key keys/firmware-signing-key.pem \
  --output securecan-gateway-signed.bin
```

#### Flashing Methods

| Method | Tool | Use Case |
|--------|------|----------|
| USB-C (Serial) | `esptool.py` | Initial flash, development |
| OTA (BLE) | SecureCAN App | Field updates |
| OTA (Wi-Fi) | SecureCAN App | Field updates (alternative) |

**USB-C Flashing:**
```bash
esptool.py --chip esp32s3 --port COM3 write_flash \
  0x0 build/securecan-gateway.bin
```

**OTA Update:**
1. Firmware binary transferred to mobile app (downloaded or sideloaded)
2. App transfers binary to gateway via BLE (MSG_FW_UPDATE chunks)
3. Gateway verifies signature, writes to OTA partition, reboots

#### Release Channels

| Channel | Frequency | Signing Key | Audience |
|---------|-----------|-------------|----------|
| Development | Per commit | Dev key (CI) | Internal developers |
| Beta | Per milestone | Dev key (CI) | Beta testers |
| Production | Per release | Production key (HSM) | All users |

#### Versioning

Format: `MAJOR.MINOR.PATCH` (semver)
- MAJOR: Incompatible protocol or hardware changes
- MINOR: Feature additions, backwards-compatible
- PATCH: Bug fixes, no functional changes

### 2. Mobile Application (React Native)

#### Build

```bash
# iOS
cd src
npm run build:ios

# Android
cd src
npm run build:android
```

#### Signing

| Platform | Method |
|----------|--------|
| iOS | Apple Developer Program certificate |
| Android | Android App Signing by Google Play or custom keystore |

#### Distribution

| Platform | MVP Distribution | Production Distribution |
|----------|-----------------|----------------------|
| iOS | TestFlight (beta) | Apple App Store |
| Android | Google Play Internal Testing | Google Play Store |
| Android (alternative) | APK sideload | APK on website |

#### Release Channels

| Channel | Build Config | Update Frequency |
|---------|-------------|-----------------|
| Debug | Debug symbols, dev server | Per commit |
| Beta | Optimised, staging config | Per milestone |
| Production | Fully optimised, release config | Per release |

#### OTA Updates

- React Native code can be updated via CodePush (or similar) without app store review
- Native module changes require full app store submission
- OTA update channel is configurable per release channel

### 3. Configuration Data

#### Bundled Configurations

The following configuration files are bundled with the mobile app:

- `configs/firewall_rules.json` — Default firewall rule set
- `configs/attack_library.json` — Attack simulation scenarios
- `configs/maintenance_rules.json` — Maintenance monitoring rules
- `configs/supported_vehicles.json` — Vehicle compatibility list
- `configs/ui.json` — UI configuration and defaults

#### Configuration Updates

- Configuration files are updated with app releases (not independently versioned in MVP)
- Phase 2: Configurable via JSON file import/export
- Phase 4: Optional cloud-synced configurations

### 4. Decoder Data (OpenDBC)

Built from OpenDBC submodule during app build:

```
1. Checkout opendbc at pinned commit
2. Run converter: dbc → json
3. Bundle decoder_data/ directory with app
4. Sign decoder data manifest
```

Decoder data version is tracked in the app's `config` table. If the bundled version differs from the installed version, the new data replaces the old on app update.

## Environment Configuration

### Development

```
App Configuration:
  BLE_DEVICE_NAME: "SecureCAN-DEV"
  LOG_LEVEL: "debug"
  ENABLE_PERFORMANCE_MONITORING: true
  ENABLE_CRASH_REPORTING: false

Gateway Configuration:
  BLE_DEVICE_NAME: "SecureCAN-DEV"
  DEBUG_MODE: true
  WATCHDOG_TIMEOUT_MS: 60000
  CAN_BITRATE: 500000
```

### Production

```
App Configuration:
  BLE_DEVICE_NAME: "SecureCAN"
  LOG_LEVEL: "warn"
  ENABLE_PERFORMANCE_MONITORING: false
  ENABLE_CRASH_REPORTING: false (opt-in)

Gateway Configuration:
  BLE_DEVICE_NAME: "SecureCAN"
  DEBUG_MODE: false
  WATCHDOG_TIMEOUT_MS: 30000
  CAN_BITRATE: 500000
```

## Rollback Procedures

### Gateway Firmware Rollback

1. Gateway maintains two bootable partitions (factory + OTA)
2. If new firmware fails to boot (watchdog reset > 3 times), bootloader reverts to factory partition
3. User can manually force factory boot via hardware button sequence
4. OTA update can push previous firmware version

### Mobile App Rollback

1. iOS: Reinstall previous version via TestFlight or App Store (if still signed)
2. Android: Sideload previous APK
3. CodePush: Rollback to previous release via CLI

## Monitoring (Opt-In)

All monitoring is opt-in and disabled by default.

| Metric | Collection | Transmission |
|--------|------------|-------------|
| App crash logs | Local only | User-initiated export |
| Performance traces | Local only | Never transmitted |
| Error diagnostics | Local only | User-initiated export |
| Usage analytics | Not collected | N/A |

---

**TODOs**

- [ ] Set up CI/CD pipeline for firmware builds
- [ ] Create firmware signing infrastructure
- [ ] Configure TestFlight and Google Play testing tracks
- [ ] Write detailed OTA update protocol documentation
- [ ] Establish firmware signing key management procedure
