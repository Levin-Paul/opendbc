# Investor FAQ — SecureCAN

## Purpose

Address common investor questions about the SecureCAN platform, market opportunity, business model, and competitive landscape.

## Market Questions

### What problem does SecureCAN solve?

Modern vehicles contain 70+ ECUs communicating over a CAN bus designed in the 1980s with no security. Vehicle owners have zero visibility into this network. Existing aftermarket tools are either cloud-dependent (uploading vehicle data to third parties), limited to basic OBD-II scan tools, or require expensive OEM diagnostic equipment. SecureCAN provides offline-first cybersecurity, integrity verification, and predictive maintenance through an affordable hardware gateway and mobile app.

### What is the addressable market?

The global automotive cybersecurity market is projected at $6.3 billion by 2027 CAGR 17.5%. The connected car market exceeds $100 billion. SecureCAN targets vehicle owners (1.4 billion vehicles worldwide), fleet operators (4 million fleets in the US alone), and aftermarket workshops (700,000 in the US).

### How does SecureCAN differentiate from competitors?

| Competitor | SecureCAN Advantage |
|------------|---------------------|
| OBD-II scanners (generic) | Real-time security analysis, not just DTC reading |
| Cloud-based telematics (Mojio, etc.) | Offline-first, privacy-preserving, no cloud dependency |
| Fleet management (Samsara, Geotab) | Lower cost, owner-focused, security-first design |
| Research tools (CANtact, USB2CAN) | Consumer-friendly UI, automated detection, maintenance |
| OEM dealership tools | 10-20x lower cost, aftermarket compatible, user-owned data |

### How does SecureCAP make money?

MVP Phase: Hardware gateway sales with bundled mobile app. Future phases: Premium features (fleet management, advanced analytics), threat intelligence subscription (optional cloud-based rule updates), white-label for fleet operators.

## Technology Questions

### Why offline-first?

Three strategic reasons: (1) Privacy — vehicle owners should not be required to upload their data to use security tools. (2) Reliability — automotive security cannot depend on cellular connectivity. (3) Competitive moat — cloud-first competitors cannot match offline performance and privacy guarantees.

### How does OpenDBC integration work?

OpenDBC is consumed as an external dependency (git submodule). SecureCAN builds a Decoder Adapter Layer that wraps OpenDBC's parser and provides a clean TypeScript interface. We never modify OpenDBC files. Vehicle support gaps are documented as product limitations. This approach allows us to leverage 200+ vehicle definitions with zero maintenance burden.

### What is the hardware cost?

Current BOM estimate is approximately $18.60 per unit at prototype quantities. Volume production (10,000+ units) is expected to reduce BOM to $12-15 per unit. Target retail price: $79-99.

## Business Questions

### What is the product roadmap?

Q3 2026: Foundation (gateway prototype, app scaffold, OpenDBC adapter). Q4 2026: MVP (threat detection, ECU verification, predictive maintenance). Q1-Q2 2027: Integrity and maintenance features, attack simulation. Q3-Q4 2027: Advanced features, scale, automotive Ethernet support.

### What regulatory compliance is required?

SecureCAN is designed as a read-only monitoring device, which places it outside the scope of NHTSA and UN R155 requirements for altering vehicle systems. As a cybersecurity tool, it is complementary to ISO 21434 workflows. Legal review for each target market is in progress.

### What is the team's background?

The SecureCAN team combines expertise in embedded systems (ESP32, CAN bus), mobile development (React Native), automotive cybersecurity (CAN pentesting), and product design. Our backgrounds span automotive OEM suppliers, cybersecurity consulting, and consumer hardware startups.

---

**TODOs**

- [ ] Develop detailed financial projections for seed round
- [ ] Create competitive landscape analysis whitepaper
- [ ] File provisional patents for key algorithms
- [ ] Establish advisory board with automotive security experts
