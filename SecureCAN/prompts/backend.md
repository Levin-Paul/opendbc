# SecureCAN Backend Development Prompt

## Context

You are building backend services for SecureCAN, an offline-first automotive cybersecurity platform. The backend consists of local services running within a React Native mobile application. There is no cloud server. All processing is local.

## Architecture

- **Language**: TypeScript (strict mode)
- **Pattern**: Layered architecture with unidirectional data flow
- **State**: React Context + useReducer
- **Storage**: SQLite via react-native-sqlite-storage
- **BLE**: react-native-ble-plx

## Key Files to Reference

- `docs/SOFTWARE_ARCHITECTURE.md` — Service layer architecture
- `docs/API_SPEC.md` — BLE protocol specification
- `docs/DATABASE.md` — SQLite schema
- `docs/OPENDBC_INTEGRATION.md` — Decoder adapter layer
- `docs/SECURITY_MODEL.md` — Authentication and encryption
- `configs/` — Configuration files and rule sets

## Service Pattern

Every service must:

1. Be a singleton module exporting async functions
2. Return `Result<T, Error>` discriminated union types
3. Include unit tests (Jest, ≥ 80% coverage)
4. Log errors with context but never expose sensitive data
5. Handle offline state gracefully (no hard cloud dependencies)

## Common Tasks

### Creating a New Service

1. Create file in `src/services/{name}.ts`
2. Implement interface with async methods
3. Register in `src/services/index.ts`
4. Write unit tests in `src/__tests__/services/{name}.test.ts`

### Adding a Database Migration

1. Create file in `src/db/migrations/{version}_{name}.sql`
2. Update `db_version` in config table
3. Migration must be additive only (no destructive changes)
4. Add rollback test

### Adding a Configuration File

1. Add JSON file to `configs/`
2. Define TypeScript interface in `src/types/configs.ts`
3. Register in `ConfigService` for loading/validation

## Rules

- Never import directly from `opendbc/` — always use the Decoder Adapter Layer
- Never store private keys in SQLite — use iOS Keychain or Android Keystore
- Never add hard cloud dependencies — all cloud features must be optional
- Every alert must include a human-readable description
- All configuration must be user-viewable and user-modifiable
- Write tests for every new service

---

**TODOs**

- [ ] Implement BLEService with reconnection logic
- [ ] Build DecoderService with vehicle auto-detection
- [ ] Create AlertService with grouping and deduplication
- [ ] Implement ConfigService with JSON schema validation
