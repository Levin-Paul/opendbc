# OpenDBC Integration — Decoder Adapter Layer

## Purpose

Define the architecture, interfaces, and constraints for integrating the OpenDBC repository as the primary CAN decoding engine in SecureCAN.

## Scope

This document covers the Decoder Adapter Layer, vehicle-specific adapters, the build process for OpenDBC artifacts, and the constraints governing OpenDBC usage.

## OpenDBC Repository

**Upstream:** https://github.com/commaai/opendbc  
**Integration:** Git submodule pinned to a specific commit  
**License:** MIT (compatible with SecureCAN licensing)  
**Status:** External dependency — read-only

### What OpenDBC Provides

- DBC (CAN database) definition files for supported vehicles
- Python-based DBC parser (`opendbc/dbc/`)
- CAN signal decoding utilities
- Vehicle fingerprint definitions

### What OpenDBC Does NOT Provide

- Real-time CAN frame capture
- CAN bus hardware interface
- Threat detection or security analysis
- Vehicle network topology
- Diagnostic protocol (UDS) parsing
- Maintenance predictions

## Integration Boundary

```
SecureCAN App                    OpenDBC (submodule)
┌─────────────────┐             ┌──────────────────────┐
│  Decoder        │             │  dbc/                │
│  Adapter Layer  │◄────────────│    *.dbc files       │
│                  │   reads     │                      │
│  ┌──────────┐   │             │  python/             │
│  │BaseDecoder│   │             │    can/              │
│  │(abstract) │   │             │    parser.py         │
│  └─────┬────┘   │             │                      │
│        │         │             │  opendbc_py/         │
│  ┌─────┴────┐   │             │    (generated)       │
│  │HondaAdapter│ │             └──────────────────────┘
│  │ToyotaAdapter││
│  │VWAdapter   │ │
│  │GenericAdapt│ │
│  └────────────┘ │
└─────────────────┘
```

## Decoder Adapter Layer

### Architecture

The Decoder Adapter Layer consists of three layers:

1. **OpenDBC Parser Wrapper** — Lowest level. Loads DBC files using OpenDBC's parser and exposes parsed definitions.
2. **Base Decoder** — Mid level. Abstract class defining the interface for all vehicle adapters. Handles frame-to-signal conversion logic common to all vehicles.
3. **Vehicle Adapters** — Highest level. Vehicle-specific implementations that handle signal naming, scaling, and make-specific behaviour.

### BaseDecoder Interface (TypeScript)

```typescript
interface SignalDef {
  name: string;
  startBit: number;
  length: number;
  isSigned: boolean;
  factor: number;
  offset: number;
  min: number;
  max: number;
  unit: string;
}

interface DecodedSignal {
  name: string;
  value: number;
  rawValue: number;
  unit: string;
  timestamp: number;
  quality: 'valid' | 'invalid' | 'stale';
}

interface CanFrame {
  timestamp: number;
  id: number;
  isExtended: boolean;
  dlc: number;
  data: Uint8Array;
}

interface VehicleProfile {
  make: string;
  model: string;
  year: number;
  fingerprint: string;
  dbcPath: string;
}

abstract class BaseDecoder {
  abstract load(profile: VehicleProfile): Promise<void>;
  abstract decode(frame: CanFrame): DecodedSignal[];
  abstract getSignal(name: string): SignalDef | null;
  abstract getSignals(): SignalDef[];
  abstract getProfile(): VehicleProfile;
  abstract getFrameCount(): number;
}
```

### Vehicle Adapter Example — Honda

```typescript
class HondaDecoder extends BaseDecoder {
  private signalMap: Map<string, SignalDef> = new Map();

  async load(profile: VehicleProfile): Promise<void> {
    // Load DBC from opendbc submodule path
    const dbcPath = `opendbc/honda_civic_touring_2016_can.dbc`;
    const rawDefs = await OpenDBCParser.load(dbcPath);
    
    // Normalise signal definitions
    for (const def of rawDefs) {
      this.signalMap.set(def.name, {
        name: def.name,
        startBit: def.start_bit,
        length: def.length,
        isSigned: def.is_signed,
        factor: def.scale,
        offset: def.offset,
        min: def.min,
        max: def.max,
        unit: def.unit,
      });
    }
  }

  decode(frame: CanFrame): DecodedSignal[] {
    // Look up message definition for this CAN ID
    const msgDef = this.getMessageDef(frame.id);
    if (!msgDef) return [];

    // Decode each signal in the message
    return msgDef.signals.map(sig => {
      const rawValue = this.extractBits(frame.data, sig.startBit, sig.length);
      const physicalValue = rawValue * sig.factor + sig.offset;
      return {
        name: sig.name,
        value: physicalValue,
        rawValue,
        unit: sig.unit,
        timestamp: frame.timestamp,
        quality: this.validateRange(physicalValue, sig) ? 'valid' : 'invalid',
      };
    });
  }

  private extractBits(data: Uint8Array, startBit: number, length: number): number {
    // Motorola or Intel bit extraction based on DBC byte order
    // Implementation follows OpenDBC's bit extraction logic
  }

  private validateRange(value: number, sig: SignalDef): boolean {
    return value >= sig.min && value <= sig.max;
  }
}
```

## Vehicle Fingerprint Detection

SecureCAN uses OpenDBC's vehicle fingerprint approach to automatically detect the connected vehicle:

1. Gateway captures first 1000 CAN frames
2. Mobile app sends frame IDs and frequencies to Decoder Adapter Layer
3. Layer iterates through OpenDBC fingerprints, finds best match
4. On match: load corresponding DBC file
5. On no match: prompt user to select vehicle manually

### Manual Vehicle Selection

If automatic detection fails (unsupported vehicle):

1. User selects make, model, year from supported vehicle list
2. If vehicle is not in OpenDBC coverage: display limitation notice
3. User can continue with generic decoder (limited signals) or use raw CAN frame view

## Build Process

OpenDBC is consumed as a pre-built dependency:

```
# In SecureCAN build pipeline:

1. Checkout opendbc submodule at pinned commit
2. Run OpenDBC's Python-based DBC-to-JSON converter
3. Convert all .dbc files to .json for React Native consumption
4. Generate vehicle fingerprint index
5. Bundle JSON artifacts with mobile app
```

The conversion step produces a `decoder_data/` directory containing:

- `signals/{make}_{model}_{year}.json` — Signal definitions per vehicle
- `fingerprints/index.json` — Vehicle fingerprint mapping
- `meta/vehicles.json` — Vehicle metadata catalog

## Testing the Integration

| Test | Description |
|------|-------------|
| DBC Loading | Each DBC file loads without error |
| Signal Decoding | Known CAN frames decode to expected values |
| Fingerprint Matching | Vehicle auto-detection returns correct profile |
| Adapter Interface | All vehicle adapters implement required methods |
| Edge Cases | Invalid CAN IDs, malformed frames, missing DBC |

## Adding a New Vehicle

1. Verify vehicle is supported in OpenDBC (check for DBC file)
2. If supported: create vehicle adapter extending BaseDecoder (if make-specific behaviour exists)
3. If not supported: document as limitation, update supported_vehicles.json
4. Test with real CAN capture from vehicle

---

**TODOs**

- [ ] Build OpenDBC-to-JSON converter script
- [ ] Implement BaseDecoder abstract class in TypeScript
- [ ] Create vehicle adapters for top 3 makes (Honda, Toyota, VW)
- [ ] Implement automatic vehicle fingerprint detection
- [ ] Write integration tests for each supported vehicle
