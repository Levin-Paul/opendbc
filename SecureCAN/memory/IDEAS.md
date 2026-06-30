# Ideas & Brainstorming

This file captures feature ideas, improvements, and research topics that are not yet committed to the roadmap. No idea is too small or too ambitious.

## Feature Ideas

### Vehicle Owner Features

- **Driving Style Analysis** — Analyse CAN signals to provide feedback on driving efficiency, braking habits, and fuel consumption patterns.
- **Trip Log** — Automatic trip detection with distance, duration, fuel consumption, and alerts summary per trip.
- **Vehicle Health Score** — Single composite score (0-100) summarising overall vehicle health based on ECU integrity, sensor status, and maintenance predictions.
- **Recall and TSB Notifications** — User can enter VIN and receive recall notifications (requires optional cloud lookup).
- **Aftermarket Device Detection** — Detect non-OEM devices on the CAN bus (e.g., aftermarket remote starters, trackers).
- **Fuse Box Map** — Interactive fuse box diagram with CAN bus component mapping.

### Fleet Operator Features

- **Geo-Fencing Alerts** — Alert when vehicle leaves defined geographic area (requires optional GPS, user opt-in).
- **Driver Behaviour Scoring** — Score drivers based on CAN signals (RPM range, speed consistency, brake harshness).
- **Maintenance Scheduling** — Automatic service appointment scheduling with integrated workshop booking API.
- **Fuel Card Integration** — Correlate fuel card data with CAN fuel level and consumption signals.
- **Compliance Reports** — Generate regulatory compliance reports for fleet safety inspections.

### Security Researcher Features

- **CAN Bus Fuzzer** — Automated CAN bus fuzzing tool to discover ECU vulnerabilities.
- **Protocol Reverse Engineering Tools** — Signal labelling tools, DBC file creator, message correlation analyser.
- **Custom Detection Rule Language** — DSL for writing complex detection rules beyond JSON conditions.
- **Vulnerability Database Integration** — Map detected CAN IDs and signals to known CVEs.
- **PCAP Export** — Export CAN captures in pcap format for Wireshark analysis.

### Workshop Features

- **Post-Repair Verification** — Compare ECU fingerprints and sensor readings before and after repair to verify work quality.
- **Service Reset Assistant** — Guide users through service interval reset procedures for common vehicles.
- **Parts Cross-Reference** — Look up OEM and aftermarket part numbers from CAN component IDs.
- **Diagnostic Trouble Code (DTC) Reader** — Read and clear DTCs via CAN (requires write-enable).
- **ECU Flashing Warning** — Warn if ECU has been reflashed with non-OEM firmware.

### Technical Improvements

- **CAN FD Support** — Full support for CAN FD (up to 8 Mbps, 64-byte payloads).
- **Automotive Ethernet (100BASE-T1)** — Support for modern vehicle networks with Ethernet backbone.
- **Multi-Gateway Synchronisation** — Multiple gateways on different CAN buses synchronised to a single time domain.
- **Machine Learning Anomaly Detection** — Train statistical baselines for each vehicle and detect subtle anomalies.
- **Compressed BLE Streaming** — Compress CAN frames before BLE transmission to reduce bandwidth.
- **Hardware Security Module (HSM)** — Dedicated secure element for key storage and cryptographic operations.
- **Wireless Firmware Update from File** — Allow firmware update from a file on the mobile device (no download required).
- **Mesh Gateway Network** — Multiple gateways in a fleet forming a local mesh network for aggregate monitoring.

## Research Topics

- **CAN Bus Electrical Characteristics** — Measure and document CAN bus voltage levels, common-mode voltages, and signal quality across vehicle makes.
- **ECU Fingerprint Stability Over Time** — Research how ECU fingerprints change with temperature, age, and firmware updates.
- **Predictive Maintenance Accuracy** — Validate trend predictions against actual failure data from fleet operators.
- **BLE Throughput Optimisation** — Benchmark BLE 5.0 Coded PHY vs 2M PHY for CAN frame streaming in vehicle environments.
- **OpenDBC Coverage Gaps** — Identify and document vehicle makes/models not covered by OpenDBC.
- **Automotive EMC Compliance** — Research CISPR 25 compliance requirements for aftermarket OBD-II devices.

## Monetisation Ideas

- **Premium Maintenance Reports** — Detailed PDF maintenance reports with parts lists and estimated costs.
- **Threat Intelligence Feed** — Optional subscription for community-sourced detection rules (opt-in, anonymised).
- **White-Label Fleet Solution** — Custom-branded version for fleet management companies.
- **Hardware Warranty Extensions** — Extended warranty on SecureCAN Gateway hardware.
- **Workshop Certification Program** — Certified SecureCAN workshops with verified integrity checks.

## UI/UX Ideas

- **Ambient Mode** — Dashboard that dims to show only critical information during driving, expands when parked.
- **Augmented Reality CAN View** — Point phone camera at engine bay, overlay live CAN signals on components.
- **Voice Alerts** — Text-to-speech for critical alerts during driving.
- **Widget Support** — iOS and Android home screen widgets showing vehicle status at a glance.
- **Apple Watch / Wear OS Companion** — Simple glanceable vehicle status on smartwatch.
- **HUD Mode** — Dashboard projected onto windscreen using phone display reflection.

---

**TODOs**

- [ ] Review ideas quarterly for roadmap candidates
- [ ] Add voting mechanism for community feature requests
- [ ] Prototype top 3 ideas as hackathon projects
