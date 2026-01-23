# Changelog

All notable changes to the Damn Vulnerable Drone project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- **Hardware Scripts Fixed**: Added validation and improved error handling to all hardware scripts:
  - `usb_exploitation.py` - Vendor/Product ID validation, specific exception handling
  - `ble_exploitation.py` - MAC address validation, specific exception handling
  - `ble_gatt_exploit.py` - MAC address and UUID validation, specific exception handling
  - `can_bus_injection.py` - Interface and message ID validation, specific exception handling
  - `can_bus_replay.py` - Interface, capture file, and message ID validation, specific exception handling
  - `serial_protocol_exploit.py` - Port and baudrate validation, specific exception handling
  - `jtag_swd_exploitation.py` - Interface, target, and action validation, specific exception handling
  - `holy_stone_ble_rce_cve_2024_52876.py` - MAC address validation, specific exception handling
- **Network Scripts Fixed**: Added validation to network attack scripts:
  - `arp_spoofing.py` - IP address and interface validation
  - `dns_spoofing.py` - Domain, IP address, and interface validation
- **Chain Executor Fixed**: Added validation and improved error handling:
  - `chain_executor.py` - Chain ID validation, parameter validation, timeout validation, file path validation
- **Additional Scripts Fixed**: Continued fixing remaining exploit scripts with helper usage and validation:
  - **Advanced Scripts**: `hail_mary_attack.py` - Helper usage
  - **Swarm Scripts**: `swarm_discovery.py` - Helper usage
  - **Orchestrator**: `payload_orchestrator.py` - Helper usage
  - **Recon Scripts**: `drone_discovery.py` - Helper usage
  - **Mission Race Condition**: Fixed connection handling in multi-threaded scenario
  - **DoS Scripts**: `ros_topic_flooding.py`, `wifi_deauth.py` - Added validation for ports, MAC addresses, counts
  - **Exfiltration Scripts**: `ftp_eavesdropping.py`, `wifi_client_data_leak.py` - Added duration and file validation
  - **Recon Scripts**: `wifi_crack.py`, `gcs_discovery.py` - Added validation for channels, SSIDs, MAC addresses, network formats
  - **Infrastructure Scripts**: `multi_vector_attack.py`, `data_interception.py`, `physical_payload_delivery.py`, `wireless_network_exploit.py` - Added coordinate, duration, and file validation
  - **Advanced Scripts**: `dji_enhanced_wifi_exploit.py`, `rf_jamming.py` - Added validation for channels, frequencies, durations
  - **Firmware Scripts**: `firmware_analysis.py` - Added file path validation
  - **MITM Scripts**: `mavlink_mitm.py` - Added connection string validation
- **GPS Spoofing Bug**: Fixed gradual mode calculation in `gps_spoofing.py` - now correctly interpolates from current position to target instead of starting from origin
- **Connection Handling**: Improved `mavlink_helper.connect_to_drone()` with specific exception handling (ConnectionError, TimeoutError)
- **Additional Scripts Fixed**: Continued fixing remaining exploit scripts with helper usage and validation:
  - **Advanced Scripts**: `hail_mary_attack.py` - Helper usage
  - **Swarm Scripts**: `swarm_discovery.py` - Helper usage
  - **Orchestrator**: `payload_orchestrator.py` - Helper usage
  - **Recon Scripts**: `drone_discovery.py` - Helper usage
  - **Mission Race Condition**: Fixed connection handling in multi-threaded scenario
  - **DoS Scripts**: `ros_topic_flooding.py`, `wifi_deauth.py` - Added validation for ports, MAC addresses, counts
  - **Exfiltration Scripts**: `ftp_eavesdropping.py`, `wifi_client_data_leak.py` - Added duration and file validation
  - **Recon Scripts**: `wifi_crack.py`, `gcs_discovery.py` - Added validation for channels, SSIDs, MAC addresses, network formats
  - **Infrastructure Scripts**: `multi_vector_attack.py`, `data_interception.py`, `physical_payload_delivery.py`, `wireless_network_exploit.py` - Added coordinate, duration, and file validation
  - **Advanced Scripts**: `dji_enhanced_wifi_exploit.py`, `rf_jamming.py` - Added validation for channels, frequencies, durations
  - **Firmware Scripts**: `firmware_analysis.py` - Added file path validation
  - **MITM Scripts**: `mavlink_mitm.py` - Added connection string validation
- **Input Validation**: Added comprehensive input validation across 40+ scripts:
  - GPS coordinates validated for valid ranges (-90 to 90 for lat, -180 to 180 for lon)
  - Altitude validated for reasonable range (-500 to 50000 meters)
  - Payload sizes validated with safety limits (max 10000 bytes)
  - Flood rates validated with limits (max 10000 msg/s)
  - Duration values validated (non-negative, warnings for > 1 hour)
  - File paths validated for write permissions and existence
  - Log IDs validated for non-negative values
  - System IDs validated (1-255 range)
  - Port numbers validated (1-65535 range)
  - Thread counts validated with limits (max 20)
  - Waypoint counts validated (max 1000)
  - Battery values validated (voltage 0-50V, current -100 to 100A, remaining 0-100%)
  - Attitude angles validated (radians and degrees)
  - Gimbal angles validated with proper ranges
  - Satellite counts validated (0-32)
  - VFR HUD parameters validated (airspeed, groundspeed, heading, throttle, altitude, climb rate)
  - URL formats validated (RTSP, HTTP, HTTPS)
  - Network parameters validated (IP addresses, hostnames)
  - MAC addresses validated with regex pattern matching
  - WiFi channels validated (1-14 for 2.4GHz, 1-165 for 5GHz)
  - SSIDs validated (max 32 characters)
  - Network interfaces validated (max 20 characters)
  - ROS topics validated (must start with /)
  - Connection strings validated (must start with udp: or tcp:)
  - Network CIDR notation validated
  - Action/mode parameters validated against allowed values
  - USB Vendor/Product IDs validated (0x0000 to 0xFFFF)
  - CAN message IDs validated (0x0000 to 0x1FFFFFFF)
  - Serial baudrates validated against standard values
  - JTAG/SWD interfaces validated (jtag, swd)
  - JTAG/SWD actions validated (dump, flash, debug)
  - BLE UUIDs validated with regex pattern
  - IP addresses validated with regex pattern
  - Domain names validated (max 255 characters)
  - Chain IDs validated (max 100 characters)
  - Parameter keys/values validated (max 100/1000 characters)
- **Error Handling**: Improved error handling across 50+ scripts:
  - Replaced broad `except Exception` with specific exceptions (ConnectionError, TimeoutError, ValueError, OSError, PermissionError, subprocess.TimeoutExpired, yaml.YAMLError)
  - Better error messages with actionable information
  - Consistent error message format: `[-] Error type: details`
  - Hardware-specific error handling (USB, BLE, CAN, Serial, JTAG/SWD access errors)
  - Permission error messages with helpful hints (e.g., "May require root/sudo")
- **Code Standardization**: Refactored key scripts to use `mavlink_helper.connect_to_drone()`:
  - `gps_spoofing.py`
  - `communication_flooding.py`
  - `buffer_overflow_cve_2024_40427.py`
  - `mavlink_inject.py`
  - `flight_log_extraction.py`
  - `packet_sniffing.py`
- **Command Validation**: Added command validation in `mavlink_inject.py` with uppercase normalization
- **Parameter Parsing**: Improved parameter parsing with proper error handling in `mavlink_inject.py`

### Changed
- **mavlink_helper.py**: Enhanced `connect_to_drone()` function with:
  - Specific exception types (ConnectionError, OSError, TimeoutError)
  - Better error messages
  - Consistent timeout handling (default 5 seconds)
- **Error Messages**: Standardized error message format across fixed scripts
- **Code Quality**: Reduced code duplication by using helper functions

### Added
- **29 New Payloads** - Comprehensive expansion of exploit library:
  - **Phase 1: High-Priority Software Payloads (11 payloads)**
    - DJI Enhanced WiFi Protocol Exploitation (CVE-2025-10250) - CRITICAL
    - MAVLink 2.0 Signature Bypass - HIGH
    - MAVLink 2.0 Extension Exploitation - MEDIUM
    - PX4 Safety Button Bypass - HIGH
    - PX4 Preflight Check Bypass - HIGH
    - Swarm Coordination Attack - HIGH
    - Swarm Controller Hijack - HIGH
    - Firmware Backdoor - HIGH
    - Adversarial Object Detection - HIGH
    - Tracking Manipulation - HIGH
    - Autonomous Decision Poisoning - HIGH
  - **Phase 2: Medium-Priority Software Payloads (10 payloads)**
    - FlyTrap Attack Framework - MEDIUM
    - ACAS-Xu System Exploitation - MEDIUM
    - Parameter Validation Bypass (ArduPilot) - MEDIUM
    - EKF Spoofing - MEDIUM
    - Swarm Discovery - MEDIUM
    - Parameter Persistence - HIGH
    - Startup Script Injection - HIGH
    - Sensor Fusion Poisoning - MEDIUM
    - Kalman Filter Attack - MEDIUM
    - RF Jamming Attacks - MEDIUM
  - **Phase 3: Hardware-Based Payloads (7 payloads)**
    - USB Exploitation - MEDIUM
    - Serial Protocol Exploitation - MEDIUM
    - BLE Exploitation - MEDIUM
    - BLE GATT Exploitation - MEDIUM
    - CAN Bus Injection - MEDIUM
    - CAN Bus Replay - MEDIUM
    - JTAG/SWD Exploitation - LOW
  - **Phase 4: Advanced Payloads (1 payload)**
    - Micro Drone Hijacking - MEDIUM
- **New Directory Structure**:
  - `exploits/advanced/` - Advanced attack frameworks
  - `exploits/swarm/` - Swarm-specific attacks
  - `exploits/persistence/` - Persistence mechanisms
  - `exploits/ai/` - AI/ML-based attacks
- **Payload Registry Updates**: All 29 new payloads registered with severity, CVSS scores, and target compatibility

### Changed
- **Total Payload Count**: Increased from 60 to 89+ payloads
- **README.md**: Updated exploit statistics to reflect 89+ payloads
- **Payload Registry**: Expanded to include all new payload categories

## [1.1.0] - 2026-01-22

### Added
- Comprehensive documentation suite:
  - README.md - Complete project overview with 72+ exploit scripts
  - USAGE_GUIDE.md - Detailed usage instructions
  - SETUP_GUIDE.md - Installation and setup guide
  - VULNERABILITIES_AND_EXPLOITS.md - Complete vulnerability analysis (40+ scenarios)
  - HARDWARE_REQUIREMENTS.md - Hardware setup guide
  - RESEARCH.md - Comprehensive 14-section research document
  - REPOSITORIES.md - GitHub repository catalog
  - SUMMARY.md - Quick reference guide
  - API_DOCUMENTATION.md - REST API reference
  - RECOMMENDATION.md - Repository selection guide
  - 2026_PAYLOADS_UPDATE.md - 2026 research findings
  - ADDITIONAL_PAYLOADS_RESEARCH.md - Additional payload research

### Features
- 89+ automated exploit scripts across 11 attack categories
- **Hail Mary Attack**: Automated multi-vector exploitation system
- 10+ real-world CVE implementations
- Dual mode operation (Lite and Full)
- Web-based management console (port 8000)
- Companion computer web interface (port 3000)
- Docker-based architecture
- MAVLink protocol integration
- QGroundControl support
- RESTful API for programmatic access

### Exploit Categories
1. **Injection Attacks** (19 scripts)
   - MAVLink command injection
   - Buffer overflow exploits (CVE-2024-40427, CVE-2024-38951, CVE-2024-38952)
   - Use-after-free (CVE-2025-9020)
   - Trajectory overflow (CVE-2025-5640)
   - Flight path manipulation (CVE-2024-29460)
   - RCE via breach return point (CVE-2024-30799)
   - Geofence bypass (CVE-2024-30800)
   - ExpressLRS UID leakage
   - Mission race conditions (CVE-2024-24254, CVE-2024-24255)

2. **Protocol Tampering** (9 scripts)
   - GPS spoofing
   - Battery spoofing
   - Attitude spoofing
   - Sensor data injection
   - VFR HUD spoofing
   - System status spoofing
   - Satellite spoofing
   - Emergency status spoofing
   - Critical error spoofing

3. **Denial of Service** (7 scripts)
   - WiFi deauthentication
   - Communication flooding
   - Geofence attacks
   - Flight termination
   - GPS offset glitching
   - Denial of takeoff
   - ROS topic flooding

4. **Exfiltration** (6 scripts)
   - Flight log extraction
   - Mission extraction
   - Parameter extraction
   - Camera feed eavesdropping
   - WiFi client data leak
   - FTP eavesdropping

5. **Reconnaissance** (7 scripts)
   - WiFi cracking (WEP/WPA2)
   - Drone discovery
   - Packet sniffing
   - Protocol fingerprinting
   - GPS telemetry tracking
   - GCS discovery
   - Companion computer discovery

6. **Man-in-the-Middle** (1 script)
   - MAVLink MITM proxy

7. **Replay Attacks** (2 scripts)
   - Command replay
   - Telemetry replay

8. **Network Attacks** (2 scripts)
   - ARP spoofing
   - DNS spoofing

9. **Firmware Attacks** (3 scripts)
   - Firmware extraction
   - Firmware analysis

10. **Hardware Attacks** (1 script)
    - Holy Stone BLE RCE (CVE-2024-52876)

11. **Infrastructure Payloads** (4 scripts)
    - Wireless network exploitation
    - Data interception
    - Physical payload delivery
    - Multi-vector attack coordination

### CVE Coverage
- CVE-2024-40427 (CVSS 7.9) - Stack buffer overflow
- CVE-2024-38952 (CVSS 7.5) - Logger buffer overflow
- CVE-2024-38951 (CVSS 6.5) - MAVLink message overflow
- CVE-2024-29460 (CVSS 6.6) - Flight path manipulation
- CVE-2024-30800 - Geofence bypass
- CVE-2024-30799 (CVSS 4.4) - Remote code execution
- CVE-2025-9020 (CVSS 4.5) - Use-after-free
- CVE-2025-5640 (High) - Trajectory overflow
- CVE-2024-52876 (CVSS 7.5) - BLE RCE (Holy Stone)
- CVE-2024-24254 (CVSS 4.2) - Race condition
- CVE-2024-24255 (CVSS 4.2) - Race condition

### System Architecture
- Flight Controller (ArduPilot SITL) - 10.13.0.2:14550
- Companion Computer (Flask Web UI) - 10.13.0.3:3000
- Ground Control Station (QGroundControl) - 10.13.0.4
- Simulator (Management Console) - 10.13.0.5:8000

### Documentation
- Comprehensive vulnerability research
- Attack scenario walkthroughs
- Hardware requirements guide
- API documentation
- Setup and usage guides
- Research papers and CVE references

### Security Research
- Based on real-world CVEs
- Academic research integration
- OWASP Top 10 Drone Security Risks coverage
- MAVLink protocol security analysis
- ArduPilot security issues
- ExpressLRS vulnerabilities
- DJI Enhanced Wi-Fi Protocol weaknesses

---

## [Unreleased]

### Added
- **Payload Orchestrator** (`exploits/payload_orchestrator.py`)
  - Comprehensive payload execution system that executes all 73+ payloads ordered by severity
  - **4-Phase Execution Flow**:
    1. **Target Discovery**: Auto-discovers and fingerprints target drones
    2. **Payload Filtering**: Filters by severity, category, and target compatibility
    3. **Payload Execution**: Executes payloads sequentially by severity (CRITICAL → HIGH → MEDIUM → LOW)
    4. **Report Generation**: Generates comprehensive JSON reports with execution results
  - **Features**:
    - Executes all 73+ payloads from all 11 attack categories
    - Severity-based execution order (CRITICAL → HIGH → MEDIUM → LOW)
    - CVSS score-based ordering within severity levels
    - Target compatibility checking (skips incompatible payloads)
    - Flexible filtering by severity and category
    - Error handling and retry logic
    - Timeout management per payload
    - Dry run mode for preview
    - Comprehensive JSON reporting
    - Progress tracking and real-time status
  - **Payload Registry** (`exploits/payload_registry.py`):
    - Complete registry of all 73+ payloads with severity, CVSS, category, and target compatibility
    - Organized by severity level for easy access
    - Helper functions for payload lookup and filtering
  - **Documentation**: `PAYLOAD_ORCHESTRATOR.md` with complete usage guide and examples
  - **Target Models**: All supported drone models (PX4, ArduPilot, DJI, Holy Stone, ExpressLRS, Parrot, Generic)
  - **Usage Examples**:
    ```bash
    # Execute all payloads
    python3 exploits/payload_orchestrator.py udp:127.0.0.1:14550
    
    # Execute only HIGH severity
    python3 exploits/payload_orchestrator.py udp:127.0.0.1:14550 --severity HIGH
    
    # Execute only injection category
    python3 exploits/payload_orchestrator.py udp:127.0.0.1:14550 --category injection
    
    # Dry run preview
    python3 exploits/payload_orchestrator.py udp:127.0.0.1:14550 --dry-run
    ```

- **Hail Mary Attack Payload** (`exploits/injection/hail_mary_attack.py`)
  - Automated multi-vector drone exploitation system inspired by Armitage's "Hail Mary" attack
  - **5-Phase Attack Flow**:
    1. **Reconnaissance**: Network scanning, device identification, connection establishment
    2. **Vulnerability Scanning**: Automated CVE scanning using vulnerability scanner
    3. **Exploit Selection**: Intelligent selection based on discovered vulnerabilities, severity, and CVSS scores
    4. **Exploit Execution**: Sequential execution of selected exploits in optimal order
    5. **Post-Exploitation**: Data extraction (parameters, missions, flight logs)
  - **Features**:
    - Supports both direct connection (`udp:127.0.0.1:14550`) and network scanning (`10.13.0.0/24`)
    - Automatic vulnerability-to-exploit mapping (10+ CVEs mapped)
    - Severity-based prioritization (CRITICAL → HIGH → MEDIUM → LOW)
    - CVSS score-based ordering within severity levels
    - Autopilot compatibility checking
    - Comprehensive JSON attack reports
    - Fallback to generic attacks if no specific vulnerabilities found
  - **Documentation**: `HAIL_MARY_ATTACK.md` with complete usage guide and examples
  - **Target Models**: ArduPilot, PX4-Autopilot, Generic MAVLink drones
  
- **README.md**: Comprehensive "Drone Manufacturer & Model Coverage Chart" section
  - Detailed breakdown by manufacturer (PX4-Autopilot, ArduPilot, DJI, Holy Stone, ExpressLRS, Parrot)
  - Complete mapping of all 73+ exploits to specific drone models and firmware versions
  - CVE-specific model information (e.g., PX4-Autopilot v1.14.3 for CVE-2024-40427)
  - Protocol-based coverage for generic attacks
  - Summary statistics by manufacturer
  - Coverage statistics showing 6+ manufacturers and 73+ exploit scripts

### Changed
- **README.md**: Added "Drone Models" column to all exploit payload tables
  - Each exploit now specifies which drone models it targets
  - Includes specific model information for CVE-based exploits (PX4-Autopilot versions, Holy Stone models, etc.)
  - Generic MAVLink/ArduPilot coverage clearly indicated
  - ExpressLRS protocol-specific exploits identified
  - WiFi-based attacks specify applicable drone models

### Planned
- Additional CVE implementations
- Enhanced infrastructure attack payloads
- AI/ML-based attack automation
- Swarm attack capabilities
- 5G network exploitation
- IoT device compromise via drone platforms

---

## Version History

- **1.1.0** (2026-01-22) - Current version with comprehensive documentation and 72+ exploit scripts
- **1.3.1** (Repository version) - Internal versioning for documentation references

---

## Notes

- This changelog follows the project's documentation standards
- All dates are in YYYY-MM-DD format
- CVE references are maintained for tracking real-world vulnerabilities
- Documentation is continuously updated as new vulnerabilities are discovered

---

**Last Updated**: January 22, 2026  
**Maintainer**: Security Research Team  
**Project**: Damn Vulnerable Drone - Professional Security Research Platform
