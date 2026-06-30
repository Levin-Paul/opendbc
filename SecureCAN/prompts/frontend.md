# SecureCAN Frontend Development Prompt

## Context

You are building the SecureCAN React Native mobile application — an offline-first interface for vehicle cybersecurity monitoring, integrity verification, and predictive maintenance.

## Architecture

- **Framework**: React Native (TypeScript, strict mode)
- **State**: React Context + useReducer
- **Navigation**: React Navigation (bottom tabs)
- **Storage**: SQLite via react-native-sqlite-storage
- **BLE**: react-native-ble-plx
- **Design**: Dark theme, high-contrast option

## Key Files to Reference

- `docs/UI_GUIDELINES.md` — Design system and component library
- `docs/USER_FLOW.md` — User flow documentation
- `docs/SOFTWARE_ARCHITECTURE.md` — Component architecture
- `configs/ui.json` — UI configuration defaults

## Component Pattern

```typescript
// Every screen and component:
// 1. Functional component with hooks
// 2. TypeScript with strict typing
// 3. No class components
// 4. Accessible (accessibilityLabel, role, etc.)
// 5. Error boundary wrapper

interface SignalCardProps {
  name: string;
  value: number;
  unit: string;
  status: 'normal' | 'warning' | 'critical';
  min: number;
  max: number;
}

const SignalCard: React.FC<SignalCardProps> = ({ name, value, unit, status, min, max }) => {
  // Implementation
};
```

## Navigation Structure

```
TabNavigator
├── Dashboard
│   ├── SignalGrid (2-column)
│   ├── CANTrafficGraph
│   └── RecentAlerts
├── Alerts
│   ├── AlertList
│   └── AlertDetail
├── Security
│   ├── ECUList → ECUDetail
│   ├── IntegritySnapshots → SnapshotCompare
│   └── FirewallStatus
├── Maintenance
│   ├── ComponentOverview → ComponentDetail
│   ├── TrendChart
│   └── PredictionTimeline
└── Settings
    ├── VehicleProfile
    ├── Configuration
    ├── DataManagement
    └── About
```

## Common Tasks

### Creating a New Screen

1. Create file in `src/screens/{name}/{name}.tsx`
2. Register in `src/navigation/index.ts`
3. Add to navigation configuration
4. Create screen-specific components in `src/components/{name}/`

### Adding a New Component

1. Create file in `src/components/{name}/{name}.tsx`
2. Define props interface
3. Include accessibility attributes
4. Add story in storybook if available
5. Support dark theme colours from design tokens

## Rules

- Dark theme only (light theme is not MVP)
- All icons must have text labels
- Touch targets minimum 44×44 pt
- Loading states use skeleton screens
- Error states show clear user-friendly messages
- Connection status must always be visible
- Pull-to-refresh on all data screens
- Support iOS VoiceOver and Android TalkBack

---

**TODOs**

- [ ] Build Dashboard screen with real-time signal cards
- [ ] Create AlertList component with severity filtering
- [ ] Implement ECU fingerprint detail view
- [ ] Build maintenance trend chart component
- [ ] Create Settings screen with configuration management
