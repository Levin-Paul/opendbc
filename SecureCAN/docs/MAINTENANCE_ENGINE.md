# Predictive Maintenance Engine — SecureCAN

## Purpose

Define the architecture, signal trend analysis methods, prediction algorithms, and alert generation logic for the predictive maintenance engine.

## Scope

This document covers the maintenance engine operating in the mobile application layer. It processes decoded CAN signals, applies trend analysis, and generates maintenance predictions with confidence scores.

## Architecture

```
┌──────────────────────────────────────────────────────┐
│             Predictive Maintenance Engine               │
│                                                         │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────┐ │
│  │ Signal       │    │ Trend        │    │ Prediction│ │
│  │ Collector    │───→│ Analyser     │───→│ Engine    │ │
│  └──────────────┘    └──────────────┘    └─────┬────┘ │
│                                                  │      │
│  ┌──────────────┐    ┌──────────────┐           │      │
│  │ Threshold    │    │ Rule         │           │      │
│  │ Database     │    │ Matcher      │───────────┘      │
│  └──────────────┘    └──────────────┘                  │
│                         │                               │
│  ┌──────────────────────▼────────────────────────┐     │
│  │              Alert Dispatcher                   │     │
│  └───────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────┘
```

## Monitored Components

The following components and signals are monitored in the MVP:

| Component | Signal | Unit | Normal Range | Trend Period |
|-----------|--------|------|--------------|-------------|
| Battery | Voltage | V | 12.0–14.8 | 30 days |
| Battery | Voltage (ignition off) | V | 12.0–12.8 | 7 days |
| DPF | Differential Pressure | kPa | 0–10 | 30 days |
| Engine | Coolant Temperature | °C | 80–110 | 7 days |
| Engine | Oil Temperature | °C | 70–120 | 7 days |
| Engine | Oil Pressure | kPa | 200–550 | 30 days |
| Transmission | Fluid Temperature | °C | 60–100 | 30 days |
| Brakes | Brake Fluid Pressure | kPa | 0–12000 | Monitor event |
| Tyres | Pressure (individual) | kPa | 180–280 | 7 days |
| Alternator | Voltage Output | V | 13.5–14.8 | 7 days |

## Trend Analysis Methods

### Linear Regression

For signals that degrade linearly (e.g., battery voltage over time):

```
y = mx + b

Where:
  y = predicted value at time x
  m = slope (rate of change per sample)
  b = intercept

Confidence = R² of regression fit
```

### Moving Average

For signals with noise that need smoothing:

```
SMA(n) = (1/n) × Σᵢ₌₀ⁿ value(i)

Where:
  n = window size (configurable, default 10 samples)
  SMA = simple moving average
```

### Rate of Change

For signals where the derivative indicates problems:

```
Δ/Δt = (value(t₂) - value(t₁)) / (t₂ - t₁)

Alert if |Δ/Δt| > threshold
```

## Prediction Generation

### Battery Health Prediction

```
Input: Battery voltage samples over 30 days
Method: Linear regression on daily minimum voltage (ignition off)
Output: Days until voltage drops below 11.8V

Example:
  Current: 12.4V
  30-day trend: -0.02V/day
  Prediction: 30 days until 11.8V threshold
  Confidence: 0.85
```

### DPF Health Prediction

```
Input: DPF differential pressure samples over 30 days
Method: Linear regression on average daily pressure
Output: Days until pressure exceeds 8 kPa threshold

Example:
  Current: 5.2 kPa
  30-day trend: +0.12 kPa/day
  Prediction: 23 days until 8 kPa threshold
  Confidence: 0.72
```

### Brake Wear Estimation

```
Input: Brake fluid pressure vs. deceleration correlation
Method: Event-based analysis per braking event
Output: Estimated remaining pad thickness percentage

Example:
  Current: 6 mm estimated thickness
  Baseline: 12 mm
  Events logged: 450
  Remaining: ~15,000 km
  Confidence: 0.60
```

## Maintenance Rules Format

Rules are defined in `configs/maintenance_rules.json`:

```json
{
  "rule_id": "string",
  "name": "string",
  "component": "string",
  "signal_name": "string",
  "analysis_method": "linear_regression | moving_average | rate_of_change | event_count",
  "parameters": {
    "window_samples": "integer",
    "window_days": "integer",
    "min_samples": "integer — minimum samples before analysis"
  },
  "thresholds": {
    "warning": "number — yellow alert threshold",
    "critical": "number — red alert threshold",
    "trend_direction": "increasing | decreasing",
    "comparison": "above | below | cross"
  },
  "prediction": {
    "enabled": "boolean",
    "target_value": "number",
    "min_confidence": "number — minimum R² or confidence score"
  },
  "alert": {
    "severity": "WARNING | CRITICAL",
    "title": "string — alert title template",
    "description": "string — alert description template",
    "category": "maintenance"
  }
}
```

## Data Storage

- Raw signal samples: stored in `decoded_signals` table with 1-hour aggregation after 7 days
- Trend results: stored in `maintenance_entries` table
- Predictions: recalculated on each new data point (throttled to once per minute)
- Historical predictions retained for accuracy comparison

## Alert Examples

**Battery Voltage Degradation**
```
WARNING | Battery voltage trending low
Current resting voltage: 12.2V (down from 12.6V 30 days ago)
Rate: -0.013V/day
Predicted below 12.0V in 15 days
Recommended action: Test battery capacity, consider replacement
```

**DPF Pressure Rising**
```
WARNING | DPF differential pressure rising
Current: 6.8 kPa (up from 3.2 kPa 30 days ago)
Rate: +0.12 kPa/day
Predicted above 10 kPa in 27 days
Recommended action: Perform DPF regeneration, check for blockage
```

---

**TODOs**

- [ ] Validate linear regression accuracy against real vehicle datasets
- [ ] Add exponential smoothing as alternative trend method
- [ ] Implement maintenance schedule calendar view
- [ ] Add support for odometer-based predictions (requires accurate mileage signal)
- [ ] Integrate with third-party parts database for cost estimation
