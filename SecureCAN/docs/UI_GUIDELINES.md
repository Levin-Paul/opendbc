# UI/UX Guidelines — SecureCAN Mobile App

## Purpose

Define the visual design language, interaction patterns, and user experience principles for the SecureCAN mobile application.

## Scope

This document covers the React Native mobile app UI for iOS and Android. It includes design tokens, component patterns, navigation structure, and accessibility requirements.

## Design Principles

1. **Clarity** — Information is presented in a structured, scannable format. No unnecessary visual noise.
2. **Transparency** — Every alert and status indicator includes context and explanation.
3. **Control** — The user always knows what the system is doing and can configure behaviour.
4. **Calm** — Security alerts are serious but not panicked. Visual design communicates urgency without alarmism.

## Brand Colours

| Token | Hex | Usage |
|-------|-----|-------|
| `--color-primary` | `#0056D6` | Primary actions, active state, links |
| `--color-primary-dark` | `#003D99` | Pressed state |
| `--color-background` | `#0D1117` | Main background (dark theme) |
| `--color-surface` | `#161B22` | Cards, panels, elevated surfaces |
| `--color-text` | `#E6EDF3` | Primary text |
| `--color-text-secondary` | `#8B949E` | Secondary text, labels |
| `--color-border` | `#30363D` | Dividers, borders |
| `--color-success` | `#3FB950` | Signal OK, authenticated, verified |
| `--color-warning` | `#D29922` | Degraded, attention needed |
| `--color-danger` | `#F85149` | Critical alert, error |
| `--color-info` | `#58A6FF` | Informational alert |

## Typography

| Token | Font | Size | Weight |
|-------|------|------|--------|
| `--font-mono` | JetBrains Mono / SF Mono | 12–14px | Regular |
| `--font-ui` | Inter / SF Pro | 13–17px | Regular, Medium, Semibold |
| `--font-heading` | Inter / SF Pro | 20–28px | Semibold |

## Component Library

### Signal Card
```
┌─────────────────────────────────────┐
│  ┌──────┐                           │
│  │ RPM  │   2450          rpm      │
│  │ icon │   ────▓███████─────      │
│  └──────┘   Normal range           │
└─────────────────────────────────────┘
```

- Signal name on left with icon
- Current value prominently displayed
- Unit of measurement
- Visual bar showing position within normal range
- Status indicator (green=normal, yellow=warning, red=critical)

### Alert Card
```
┌─────────────────────────────────────┐
│  ⚠ WARNING  │  2 min ago           │
│  CAN Message Injection Detected    │
│  ECU 0x1A3 sent 200 msgs in 1s     │
│  (normal max: 50)                   │
│  [View Details] [Acknowledge]      │
└─────────────────────────────────────┘
```

- Severity badge (colour-coded)
- Relative timestamp
- Concise alert title
- Evidence summary
- Action buttons

### Navigation

Tab-based navigation with 5 bottom tabs:

1. **Dashboard** — Live signal overview, CAN traffic, vehicle status
2. **Alerts** — Alert history with filter and search
3. **Security** — ECU fingerprints, integrity snapshots, firewall status
4. **Maintenance** — Trend charts, predictions, maintenance log
5. **Settings** — Vehicle profile, configuration, data management, about

## Screen Layouts

### Dashboard Layout

```
┌──────────────────────────────────────┐
│ Status Bar                           │
├──────────────────────────────────────┤
│ Vehicle Name                     ●●  │  <- Connection indicator
├──────────────────────────────────────┤
│ ┌──────────┐ ┌──────────┐           │
│ │ Speed    │ │ RPM      │           │  <- Signal cards (2-column grid)
│ │ 65 km/h  │ │ 2450     │           │
│ └──────────┘ └──────────┘           │
│ ┌──────────┐ ┌──────────┐           │
│ │ Coolant  │ │ Fuel     │           │
│ │ 90 °C    │ │ 55%      │           │
│ └──────────┘ └──────────┘           │
├──────────────────────────────────────┤
│ Recent Alerts (2 shown, tap for all) │
├──────────────────────────────────────┤
│ CAN Traffic Graph                    │  <- Real-time message rate chart
└──────────────────────────────────────┘
```

### Alerts Screen

```
┌──────────────────────────────────────┐
│ ← Back        Alerts        🔍 Filter │
├──────────────────────────────────────┤
│ [Active] [Acknowledged] [All]       │  <- Segmented control
│ [All] [Threat] [Maint] [System]     │  <- Category chips
├──────────────────────────────────────┤
│ CRITICAL  │ CAN bus flood detected   │  <- Alert rows
│ WARNING   │ Battery voltage low      │
│ INFO      │ ECU fingerprint match    │
│ ...                                  │
└──────────────────────────────────────┘
```

## Dark Mode

- Dark theme is the default and only theme for MVP
- High-contrast mode available for direct sunlight readability
- Light theme planned for Phase 2

## Accessibility

- Minimum touch target: 44×44 pt
- All icons paired with text labels
- Screen reader support (iOS VoiceOver, Android TalkBack)
- Alert announcements via OS accessibility API
- Minimum contrast ratio: 4.5:1 for normal text, 3:1 for large text

## Loading States

- Skeleton screens during initial load
- Pull-to-refresh for manual data refresh
- Connection status indicator always visible
- Graceful degradation when gateway disconnected

## Error States

- Inline error messages next to affected component
- Retry button for transient failures
- Clear explanation of what went wrong
- Offline mode indicator when BLE/Wi-Fi unavailable

---

**TODOs**

- [ ] Create Figma design system with all components
- [ ] Implement dark theme colour tokens in React Native
- [ ] Build component storybook for visual regression testing
- [ ] Conduct accessibility audit with real devices
