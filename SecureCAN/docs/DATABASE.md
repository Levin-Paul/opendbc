# Database Schema — SecureCAN Local Storage

## Purpose

Define the SQLite database schema for the SecureCAN mobile application, including all tables, indices, triggers, and migration policies.

## Scope

This document covers the local SQLite database that stores vehicle data, alerts, configurations, and user preferences on the mobile device. This is the sole persistent storage layer for all vehicle data.

## Database Engine

- SQLite 3.x via `react-native-sqlite-storage`
- WAL (Write-Ahead Logging) mode for concurrent read performance
- Foreign keys enforced via `PRAGMA foreign_keys = ON`

## Schema

### Table: vehicles

```sql
CREATE TABLE vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vin TEXT UNIQUE,
    make TEXT NOT NULL,
    model TEXT NOT NULL,
    year INTEGER,
    platform TEXT,
    opendbc_car_fingerprint TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);
```

### Table: sessions

```sql
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER NOT NULL,
    started_at TEXT NOT NULL DEFAULT (datetime('now')),
    ended_at TEXT,
    gateway_fw_version TEXT,
    frame_count INTEGER DEFAULT 0,
    error_count INTEGER DEFAULT 0,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
);
```

### Table: can_frames

```sql
CREATE TABLE can_frames (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    timestamp_ms INTEGER NOT NULL,
    can_id INTEGER NOT NULL,
    is_extended INTEGER NOT NULL DEFAULT 0,
    dlc INTEGER NOT NULL,
    data_hex TEXT NOT NULL,
    bus INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);

CREATE INDEX idx_can_frames_session ON can_frames(session_id);
CREATE INDEX idx_can_frames_can_id ON can_frames(can_id);
CREATE INDEX idx_can_frames_timestamp ON can_frames(timestamp_ms);
```

### Table: decoded_signals

```sql
CREATE TABLE decoded_signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    frame_id INTEGER NOT NULL,
    signal_name TEXT NOT NULL,
    signal_value REAL,
    signal_unit TEXT,
    signal_raw REAL,
    FOREIGN KEY (frame_id) REFERENCES can_frames(id)
);

CREATE INDEX idx_decoded_signals_name ON decoded_signals(signal_name);
CREATE INDEX idx_decoded_signals_frame ON decoded_signals(frame_id);
```

### Table: alerts

```sql
CREATE TABLE alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    timestamp_ms INTEGER NOT NULL,
    severity TEXT NOT NULL CHECK (severity IN ('INFO', 'WARNING', 'CRITICAL', 'EMERGENCY')),
    category TEXT NOT NULL CHECK (category IN ('threat', 'integrity', 'maintenance', 'system', 'sensor')),
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    affected_component TEXT,
    detection_rule TEXT,
    evidence_summary TEXT,
    recommended_action TEXT,
    acknowledged INTEGER NOT NULL DEFAULT 0,
    acknowledged_at TEXT,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);

CREATE INDEX idx_alerts_severity ON alerts(severity);
CREATE INDEX idx_alerts_category ON alerts(category);
CREATE INDEX idx_alerts_timestamp ON alerts(timestamp_ms);
```

### Table: ecu_fingerprints

```sql
CREATE TABLE ecu_fingerprints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER NOT NULL,
    ecu_name TEXT NOT NULL,
    can_id INTEGER NOT NULL,
    fingerprint_hash TEXT NOT NULL,
    message_pattern TEXT,
    response_pattern TEXT,
    is_baseline INTEGER NOT NULL DEFAULT 0,
    baseline_at TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
);

CREATE INDEX idx_ecu_fingerprints_vehicle ON ecu_fingerprints(vehicle_id);
```

### Table: maintenance_entries

```sql
CREATE TABLE maintenance_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER NOT NULL,
    component TEXT NOT NULL,
    signal_name TEXT NOT NULL,
    predicted_failure_at TEXT,
    confidence REAL CHECK (confidence >= 0 AND confidence <= 1),
    current_trend TEXT,
    trend_direction TEXT CHECK (trend_direction IN ('increasing', 'decreasing', 'stable', 'unknown')),
    threshold_value REAL,
    current_value REAL,
    rule_id TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
);

CREATE INDEX idx_maintenance_component ON maintenance_entries(component);
```

### Table: firewall_log

```sql
CREATE TABLE firewall_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    timestamp_ms INTEGER NOT NULL,
    can_id INTEGER NOT NULL,
    action TEXT NOT NULL CHECK (action IN ('allow', 'block', 'drop')),
    rule_id TEXT,
    reason TEXT,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);

CREATE INDEX idx_firewall_log_session ON firewall_log(session_id);
```

### Table: config

```sql
CREATE TABLE config (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);
```

### Table: attack_simulation_results

```sql
CREATE TABLE attack_simulation_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER NOT NULL,
    scenario_id TEXT NOT NULL,
    scenario_name TEXT NOT NULL,
    started_at TEXT NOT NULL,
    completed_at TEXT,
    frames_injected INTEGER DEFAULT 0,
    detections_triggered INTEGER DEFAULT 0,
    detection_rate REAL,
    notes TEXT,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
);
```

## Migration Policy

- Migrations use sequential numbered SQL files in `src/db/migrations/`
- Current migration version stored in `config` table with key `db_version`
- All migrations are additive only — no destructive schema changes
- Schema version rollback is NOT supported; forward-only

## Data Retention

| Table | Default Retention | Configurable |
|-------|-------------------|--------------|
| can_frames | 7 days | Yes |
| decoded_signals | 7 days | Yes |
| alerts | 90 days | Yes |
| ecu_fingerprints | Permanent | No |
| maintenance_entries | Permanent | No |
| firewall_log | 14 days | Yes |
| sessions | 90 days | Yes |
| attack_simulation_results | Permanent | Yes |

## Purging Strategy

- Old records are purged automatically via React Native `AppState` background task
- Purge runs once per app cold start and once per day while active
- User can trigger manual purge from Settings

## Encryption

- The SQLite database file is NOT encrypted by default in MVP
- Optional SQLCipher integration planned for Phase 2
- User authentication keys are stored in iOS Keychain / Android Keystore, never in SQLite

---

**TODOs**

- [ ] Implement migration framework with rollback protection
- [ ] Add database backup/restore functionality
- [ ] Evaluate SQLCipher integration for encrypted storage
- [ ] Define database performance benchmarks with 1M+ frame datasets
