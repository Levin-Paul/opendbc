# SecureCAN UI/UX Design Prompt

## Context

You are designing the user interface for SecureCAN — a vehicle cybersecurity and predictive maintenance mobile app. The audience includes vehicle owners, fleet operators, and security researchers.

## Design Principles

1. **Clarity** — Structured, scannable information. No unnecessary visual noise.
2. **Transparency** — Every alert includes context and explanation.
3. **Control** — User always knows what the system is doing.
4. **Calm** — Serious alerts without panic. Colour communicates urgency.

## Key Files to Reference

- `docs/UI_GUIDELINES.md` — Full design system, components, layouts
- `docs/USER_FLOW.md` — User flows and screen descriptions
- `configs/ui.json` — UI configuration defaults

## Design System

### Colour Tokens

```
--color-primary: #0056D6
--color-background: #0D1117
--color-surface: #161B22
--color-text: #E6EDF3
--color-text-secondary: #8B949E
--color-success: #3FB950
--color-warning: #D29922
--color-danger: #F85149
--color-info: #58A6FF
```

### Typography

- Mono: JetBrains Mono (CAN data, hex values)
- UI: Inter (body text, labels)
- Headings: Inter Semibold

### Component Library to Build

| Component | Description |
|-----------|-------------|
| SignalCard | Real-time signal display with range bar |
| AlertCard | Alert summary with severity badge |
| AlertDetail | Full alert information |
| ConnectionIndicator | BLE/Wi-Fi connection status |
| SeverityBadge | Colour-coded severity label |
| TrendChart | Signal history line chart |
| ECUCard | ECU fingerprint summary |
| ConfigEditor | JSON configuration viewer |
| CANFrameViewer | Raw CAN frame display with filter |

## Screens to Design

### Dashboard
- Signal cards in 2-column grid
- CAN traffic rate chart
- Recent alerts panel
- Connection status always visible
- Pull-to-refresh

### Alerts
- Segmented control: Active / Acknowledged / All
- Category chips: All / Threat / Maintenance / System
- Alert rows with severity icon, title, timestamp
- Tap for detail view
- Filter and search

### Security
- ECU list with fingerprint status
- Integrity snapshot comparison
- Firewall rule status
- Attack simulation launcher

### Maintenance
- Component overview cards
- Trend chart with prediction line
- Maintenance timeline
- Recommended actions list

### Settings
- Vehicle profile selection
- Configuration file editor
- Data management (export, purge)
- Gateway firmware update
- Security (key management, pairing)

## Deliverables

- Figma design system with all components
- Component documentation with states (default, loading, error, empty)
- Screen flow diagrams connecting user flows
- Accessibility annotations for each component

---

**TODOs**

- [ ] Create Figma design system with colour, typography, spacing tokens
- [ ] Design all screens for MVP (Dashboard, Alerts, Security, Maintenance, Settings)
- [ ] Build component library in React Native
- [ ] Create interactive prototype for usability testing
- [ ] Document all component states and edge cases
