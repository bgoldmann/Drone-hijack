# 🚁 Damn Vulnerable Drone - Professional Security Research Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)
[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](https://github.com/yourusername/damn-vulnerable-drone)

> **A comprehensive, intentionally vulnerable drone simulator designed for security research, penetration testing, and educational purposes. Master drone security through hands-on exploitation of real-world vulnerabilities.**

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [What You Can Do](#-what-you-can-do)
- [Attack Payloads & Exploits](#-attack-payloads--exploits)
- [Drone Manufacturer & Model Coverage Chart](#-drone-manufacturer--model-coverage-chart)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage Guide](#-usage-guide)
- [System Architecture](#-system-architecture)
- [Documentation](#-documentation)
- [Statistics](#-statistics)
- [Legal Notice](#-legal-notice)
- [Contributing](#-contributing)
- [Resources](#-resources)

---

## 🎯 Overview

**Damn Vulnerable Drone** is a professional-grade security research platform that simulates a vulnerable drone system with **72+ automated exploit scripts** covering **11 attack categories** and **10+ real-world CVEs**. Built on Docker, it provides a safe, isolated environment for learning drone security, penetration testing, and vulnerability research.

### Why This Project?

- ✅ **Real-World Vulnerabilities**: Exploits based on actual CVEs affecting commercial drone systems
- ✅ **Comprehensive Coverage**: 40+ attack scenarios across network, firmware, hardware, and protocol layers
- ✅ **Educational Focus**: Step-by-step guides, detailed documentation, and hands-on learning
- ✅ **Production-Ready**: Professional Docker-based architecture with web interfaces
- ✅ **Research-Backed**: Based on academic research and security advisories

---

## ✨ Key Features

### 🎓 Educational Platform
- **Interactive Web Console**: Management dashboard at `http://localhost:8000`
- **Companion Computer Interface**: Web UI at `http://localhost:3000`
- **Attack Scenario Guides**: Detailed YAML-based walkthroughs for each exploit
- **Progress Tracking**: Built-in system to track your learning progress

### 🔧 Technical Capabilities
- **Dual Mode Operation**: Lite mode (no GPU) or Full mode (3D Gazebo simulation)
- **Docker-Based**: Isolated, reproducible environment
- **MAVLink Protocol**: Full ArduPilot SITL integration
- **QGroundControl Support**: Real ground control station integration
- **RESTful API**: Programmatic access to all features

### 🛡️ Security Research
- **72+ Exploit Scripts**: Automated Python scripts for all attack vectors
- **10+ Real CVEs**: Proof-of-concept exploits for documented vulnerabilities
- **Attack Chains**: Multi-stage attack orchestration
- **Vulnerability Scanner**: Automated security assessment tools

---

## 🎮 What You Can Do

### 1. **Learn Drone Security**
- Understand common drone vulnerabilities and attack vectors
- Practice penetration testing in a safe environment
- Learn MAVLink protocol security issues
- Study real-world CVE implementations

### 2. **Conduct Security Research**
- Test new attack techniques
- Develop custom exploit scripts
- Analyze drone communication protocols
- Research firmware vulnerabilities

### 3. **Train & Certify**
- Prepare for drone security certifications
- Train security teams on drone threats
- Develop defensive strategies
- Practice incident response

### 4. **Develop Secure Drones**
- Understand attack vectors to build better defenses
- Test security implementations
- Validate security controls
- Follow secure development practices

---

## 💣 Attack Payloads & Exploits

### 📊 Exploit Statistics

- **Total Exploit Scripts**: 73+
- **Attack Categories**: 11
- **Real-World CVEs**: 10+
- **Attack Scenarios**: 40+
- **Documented Vulnerabilities**: 46

### 🗂️ Exploit Categories

#### 1. **Injection Attacks** (20 scripts)
Inject malicious commands and data into drone systems.

| Exploit | Description | CVE | Drone Models |
|---------|-------------|-----|--------------|
| `hail_mary_attack.py` | Automated multi-vector exploitation (recon, scan, exploit) | Multiple | ArduPilot, PX4, Generic MAVLink drones |
| `mavlink_inject.py` | Inject MAVLink commands | - | ArduPilot, PX4, Generic MAVLink drones |
| `waypoint_override.py` | Override mission waypoints | - | ArduPilot, PX4, Generic MAVLink drones |
| `buffer_overflow_cve_2024_40427.py` | Stack buffer overflow | CVE-2024-40427 (CVSS 7.9) | PX4-Autopilot v1.14.3 |
| `buffer_overflow_cve_2024_38951.py` | MAVLink message overflow | CVE-2024-38951 (CVSS 6.5) | PX4-Autopilot v1.12.3, v1.14.3 |
| `logger_overflow_cve_2024_38952.py` | Logger buffer overflow | CVE-2024-38952 (CVSS 7.5) | PX4-Autopilot v1.12.3, v1.14.3 |
| `use_after_free_cve_2025_9020.py` | Use-after-free vulnerability | CVE-2025-9020 (CVSS 4.5) | PX4-Autopilot up to v1.15.4 |
| `trajectory_overflow_cve_2025_5640.py` | Trajectory waypoint overflow | CVE-2025-5640 (High) | PX4-Autopilot v1.12.3 |
| `flight_path_manipulation_cve_2024_29460.py` | Flight path manipulation | CVE-2024-29460 (CVSS 6.6) | PX4-Autopilot |
| `breach_return_point_rce_cve_2024_30799.py` | Remote code execution | CVE-2024-30799 (CVSS 4.4) | PX4-Autopilot |
| `geofence_bypass.py` | Bypass geofence restrictions | CVE-2024-30800 | PX4-Autopilot, ArduPilot |
| `expresslrs_uid_leakage.py` | ExpressLRS UID leakage | - | FPV drones with ExpressLRS protocol |
| `mission_race_condition.py` | Race condition in missions | CVE-2024-24254, CVE-2024-24255 | PX4-Autopilot |
| `parameter_manipulation.py` | Modify critical parameters | - | ArduPilot, PX4, Generic MAVLink drones |
| `return_to_home_override.py` | Override home position | - | ArduPilot, PX4, Generic MAVLink drones |
| `gimbal_takeover.py` | Camera gimbal control | - | ArduPilot, PX4, Generic MAVLink drones |
| `flight_mode_injection.py` | Force flight mode changes | - | ArduPilot, PX4, Generic MAVLink drones |
| `gcs_spoofing.py` | Ground control station spoofing | - | ArduPilot, PX4, Generic MAVLink drones |
| `web_ui_brute_force.py` | Brute force web UI login | - | Drones with companion computer web UI |
| `companion_computer_exploit.py` | Companion computer exploitation | - | Drones with companion computer (Raspberry Pi, etc.) |

**Usage Example:**
```bash
# Hail Mary Attack - Automated comprehensive exploitation
python3 exploits/injection/hail_mary_attack.py udp:127.0.0.1:14550
python3 exploits/injection/hail_mary_attack.py 10.13.0.0/24 --output report.json

# Buffer overflow attack
python3 exploits/injection/buffer_overflow_cve_2024_40427.py udp:127.0.0.1:14550

# Geofence bypass
python3 exploits/injection/geofence_bypass.py udp:127.0.0.1:14550 disable
```

#### 2. **Protocol Tampering** (9 scripts)
Manipulate telemetry and sensor data to mislead operators.

| Exploit | Description | Drone Models |
|---------|-------------|--------------|
| `gps_spoofing.py` | Inject fake GPS coordinates | ArduPilot, PX4, Generic MAVLink drones |
| `battery_spoofing.py` | Spoof battery telemetry | ArduPilot, PX4, Generic MAVLink drones |
| `attitude_spoofing.py` | Inject false attitude data | ArduPilot, PX4, Generic MAVLink drones |
| `sensor_data_injection.py` | Inject IMU/barometer/magnetometer data | ArduPilot, PX4, Generic MAVLink drones |
| `vfr_hud_spoofing.py` | Spoof Visual Flight Rules HUD data | ArduPilot, PX4, Generic MAVLink drones |
| `system_status_spoofing.py` | Manipulate system status messages | ArduPilot, PX4, Generic MAVLink drones |
| `satellite_spoofing.py` | Falsify GPS satellite count | ArduPilot, PX4, Generic MAVLink drones |
| `emergency_status_spoofing.py` | Inject false emergency status | ArduPilot, PX4, Generic MAVLink drones |
| `critical_error_spoofing.py` | Spoof critical error messages | ArduPilot, PX4, Generic MAVLink drones |

**Usage Example:**
```bash
# GPS spoofing attack
python3 exploits/tampering/gps_spoofing.py udp:127.0.0.1:14550 37.7749 -122.4194 100

# Battery spoofing
python3 exploits/tampering/battery_spoofing.py udp:127.0.0.1:14550 10.0 0 10 --trigger-warning
```

#### 3. **Denial of Service (DoS)** (7 scripts)
Disrupt drone operations and communication.

| Exploit | Description | Drone Models |
|---------|-------------|--------------|
| `wifi_deauth.py` | WiFi deauthentication attack | WiFi-enabled drones (DJI, Parrot, etc.) |
| `communication_flooding.py` | Flood MAVLink channel | ArduPilot, PX4, Generic MAVLink drones |
| `geofence_attack.py` | Trigger false geofence violations | ArduPilot, PX4, Generic MAVLink drones |
| `flight_termination.py` | Send flight termination command | ArduPilot, PX4, Generic MAVLink drones |
| `gps_offset_glitching.py` | GPS offset glitching | ArduPilot, PX4, Generic MAVLink drones |
| `denial_of_takeoff.py` | Prevent drone from taking off | ArduPilot, PX4, Generic MAVLink drones |
| `ros_topic_flooding.py` | ROS topic flooding | ROS-based drones (companion computers) |

**Usage Example:**
```bash
# Communication flooding
python3 exploits/dos/communication_flooding.py udp:127.0.0.1:14550 --duration 60

# WiFi deauthentication
python3 exploits/dos/wifi_deauth.py wlan0mon 192.168.13.1
```

#### 4. **Exfiltration** (6 scripts)
Extract sensitive data from drone systems.

| Exploit | Description | Drone Models |
|---------|-------------|--------------|
| `flight_log_extraction.py` | Extract ArduPilot BIN logs | ArduPilot, PX4, Generic MAVLink drones |
| `mission_extraction.py` | Download mission waypoints | ArduPilot, PX4, Generic MAVLink drones |
| `parameter_extraction.py` | Extract all system parameters | ArduPilot, PX4, Generic MAVLink drones |
| `camera_feed_eavesdropping.py` | Intercept RTSP camera streams | Drones with RTSP camera streaming |
| `wifi_client_data_leak.py` | Extract data from WiFi clients | WiFi-enabled drones |
| `ftp_eavesdropping.py` | Intercept FTP traffic and credentials | Drones with FTP services |

**Usage Example:**
```bash
# Extract flight logs
python3 exploits/exfiltration/flight_log_extraction.py udp:127.0.0.1:14550

# Extract mission data
python3 exploits/exfiltration/mission_extraction.py udp:127.0.0.1:14550 mission.json
```

#### 5. **Reconnaissance** (7 scripts)
Gather intelligence about drone systems.

| Exploit | Description | Drone Models |
|---------|-------------|--------------|
| `wifi_crack.py` | Crack WiFi passwords (WEP/WPA2) | WiFi-enabled drones (DJI Spark, Mavic Air, Mini series) |
| `drone_discovery.py` | Discover drones on network | All MAVLink-compatible drones |
| `packet_sniffing.py` | Capture and analyze MAVLink traffic | ArduPilot, PX4, Generic MAVLink drones |
| `protocol_fingerprinting.py` | Identify system capabilities | ArduPilot, PX4, Generic MAVLink drones |
| `gps_telemetry_tracking.py` | Track drone GPS position in real-time | GPS-enabled drones |
| `gcs_discovery.py` | Ground control station discovery | All MAVLink-compatible drones |
| `companion_computer_discovery.py` | Companion computer service discovery | Drones with companion computers |

**Usage Example:**
```bash
# WiFi password cracking
python3 exploits/recon/wifi_crack.py wlan0mon --target SSID --mode wep

# Packet sniffing
python3 exploits/recon/packet_sniffing.py udp:127.0.0.1:14550 --duration 300
```

#### 6. **Man-in-the-Middle (MITM)** (1 script)
Intercept and manipulate communications.

| Exploit | Description | Drone Models |
|---------|-------------|--------------|
| `mavlink_mitm.py` | MAVLink man-in-the-middle proxy | ArduPilot, PX4, Generic MAVLink drones |

**Usage Example:**
```bash
# MITM attack
python3 exploits/mitm/mavlink_mitm.py udp:127.0.0.1:14550 udp:10.13.0.2:14550
```

#### 7. **Replay Attacks** (2 scripts)
Capture and replay commands.

| Exploit | Description | Drone Models |
|---------|-------------|--------------|
| `command_replay.py` | Capture and replay MAVLink commands | ArduPilot, PX4, Generic MAVLink drones |
| `telemetry_replay.py` | Telemetry replay attack | ArduPilot, PX4, Generic MAVLink drones |

**Usage Example:**
```bash
# Capture commands
python3 exploits/replay/command_replay.py udp:127.0.0.1:14550 capture commands.json 60

# Replay commands
python3 exploits/replay/command_replay.py udp:127.0.0.1:14550 replay commands.json
```

#### 8. **Network Attacks** (2 scripts)
Network-level exploitation.

| Exploit | Description | Drone Models |
|---------|-------------|--------------|
| `arp_spoofing.py` | ARP spoofing for MITM attacks | Network-connected drones |
| `dns_spoofing.py` | DNS spoofing | Network-connected drones |

#### 9. **Firmware Attacks** (3 scripts)
Firmware-level exploitation.

| Exploit | Description | Drone Models |
|---------|-------------|--------------|
| `firmware_extraction.py` | Extract firmware from flight controller | ArduPilot, PX4, Generic flight controllers |
| `firmware_analysis.py` | Analyze firmware binaries for vulnerabilities | All drone firmware types |

#### 10. **Hardware Attacks** (1 script)
Hardware-level exploitation.

| Exploit | Description | CVE | Drone Models |
|---------|-------------|-----|--------------|
| `holy_stone_ble_rce_cve_2024_52876.py` | Holy Stone BLE RCE | CVE-2024-52876 (CVSS 7.5) | Holy Stone drones with HSRID01 Remote ID Module |

#### 11. **Infrastructure Payloads** (4 scripts)
Advanced infrastructure attack vectors (2026 research).

| Exploit | Description | Drone Models |
|---------|-------------|--------------|
| `wireless_network_exploit.py` | Wireless network exploitation from drone | Any drone capable of carrying payload (2026 research) |
| `data_interception.py` | Intercept wireless communications | Any drone with wireless interception capability |
| `physical_payload_delivery.py` | Simulate physical payload delivery | Any drone with payload delivery capability |
| `multi_vector_attack.py` | Multi-vector infrastructure attack coordination | Any drone platform (coordinated attacks) |

---

## 📊 Drone Manufacturer & Model Coverage Chart

This comprehensive chart shows which drone manufacturers and models are covered by each exploit payload.

### By Manufacturer

#### **PX4-Autopilot** (DroneDev Foundation)
| Exploit | Model/Firmware Version | CVE |
|---------|------------------------|-----|
| `buffer_overflow_cve_2024_40427.py` | PX4-Autopilot v1.14.3 | CVE-2024-40427 |
| `buffer_overflow_cve_2024_38951.py` | PX4-Autopilot v1.12.3, v1.14.3 | CVE-2024-38951 |
| `logger_overflow_cve_2024_38952.py` | PX4-Autopilot v1.12.3, v1.14.3 | CVE-2024-38952 |
| `use_after_free_cve_2025_9020.py` | PX4-Autopilot up to v1.15.4 | CVE-2025-9020 |
| `trajectory_overflow_cve_2025_5640.py` | PX4-Autopilot v1.12.3 | CVE-2025-5640 |
| `flight_path_manipulation_cve_2024_29460.py` | PX4-Autopilot (all versions) | CVE-2024-29460 |
| `breach_return_point_rce_cve_2024_30799.py` | PX4-Autopilot (all versions) | CVE-2024-30799 |
| `geofence_bypass.py` | PX4-Autopilot (all versions) | CVE-2024-30800 |
| `mission_race_condition.py` | PX4-Autopilot (all versions) | CVE-2024-24254, CVE-2024-24255 |
| `hail_mary_attack.py` | All PX4-based drones | Automated multi-vector attack |
| `mavlink_inject.py` | All PX4-based drones | - |
| `waypoint_override.py` | All PX4-based drones | - |
| `parameter_manipulation.py` | All PX4-based drones | - |
| `return_to_home_override.py` | All PX4-based drones | - |
| `gimbal_takeover.py` | All PX4-based drones | - |
| `flight_mode_injection.py` | All PX4-based drones | - |
| `gcs_spoofing.py` | All PX4-based drones | - |
| `gps_spoofing.py` | All PX4-based drones | - |
| `battery_spoofing.py` | All PX4-based drones | - |
| `attitude_spoofing.py` | All PX4-based drones | - |
| `sensor_data_injection.py` | All PX4-based drones | - |
| `vfr_hud_spoofing.py` | All PX4-based drones | - |
| `system_status_spoofing.py` | All PX4-based drones | - |
| `satellite_spoofing.py` | All PX4-based drones | - |
| `emergency_status_spoofing.py` | All PX4-based drones | - |
| `critical_error_spoofing.py` | All PX4-based drones | - |
| `communication_flooding.py` | All PX4-based drones | - |
| `geofence_attack.py` | All PX4-based drones | - |
| `flight_termination.py` | All PX4-based drones | - |
| `gps_offset_glitching.py` | All PX4-based drones | - |
| `denial_of_takeoff.py` | All PX4-based drones | - |
| `flight_log_extraction.py` | All PX4-based drones | - |
| `mission_extraction.py` | All PX4-based drones | - |
| `parameter_extraction.py` | All PX4-based drones | - |
| `packet_sniffing.py` | All PX4-based drones | - |
| `protocol_fingerprinting.py` | All PX4-based drones | - |
| `mavlink_mitm.py` | All PX4-based drones | - |
| `command_replay.py` | All PX4-based drones | - |
| `telemetry_replay.py` | All PX4-based drones | - |
| `firmware_extraction.py` | All PX4-based drones | - |

#### **ArduPilot** (ArduPilot Development Team)
| Exploit | Model/Firmware Version | Notes |
|---------|------------------------|-------|
| `hail_mary_attack.py` | All ArduPilot-based drones | Automated multi-vector attack |
| `hail_mary_attack.py` | All ArduPilot-based drones | Automated multi-vector attack |
| `mavlink_inject.py` | All ArduPilot-based drones | Generic MAVLink |
| `waypoint_override.py` | All ArduPilot-based drones | Generic MAVLink |
| `geofence_bypass.py` | All ArduPilot-based drones | Generic MAVLink |
| `parameter_manipulation.py` | All ArduPilot-based drones | Generic MAVLink |
| `return_to_home_override.py` | All ArduPilot-based drones | Generic MAVLink |
| `gimbal_takeover.py` | All ArduPilot-based drones | Generic MAVLink |
| `flight_mode_injection.py` | All ArduPilot-based drones | Generic MAVLink |
| `gcs_spoofing.py` | All ArduPilot-based drones | Generic MAVLink |
| `gps_spoofing.py` | All ArduPilot-based drones | Generic MAVLink |
| `battery_spoofing.py` | All ArduPilot-based drones | Generic MAVLink |
| `attitude_spoofing.py` | All ArduPilot-based drones | Generic MAVLink |
| `sensor_data_injection.py` | All ArduPilot-based drones | Generic MAVLink |
| `vfr_hud_spoofing.py` | All ArduPilot-based drones | Generic MAVLink |
| `system_status_spoofing.py` | All ArduPilot-based drones | Generic MAVLink |
| `satellite_spoofing.py` | All ArduPilot-based drones | Generic MAVLink |
| `emergency_status_spoofing.py` | All ArduPilot-based drones | Generic MAVLink |
| `critical_error_spoofing.py` | All ArduPilot-based drones | Generic MAVLink |
| `communication_flooding.py` | All ArduPilot-based drones | Generic MAVLink |
| `geofence_attack.py` | All ArduPilot-based drones | Generic MAVLink |
| `flight_termination.py` | All ArduPilot-based drones | Generic MAVLink |
| `gps_offset_glitching.py` | All ArduPilot-based drones | Generic MAVLink |
| `denial_of_takeoff.py` | All ArduPilot-based drones | Generic MAVLink |
| `flight_log_extraction.py` | All ArduPilot-based drones | Generic MAVLink |
| `mission_extraction.py` | All ArduPilot-based drones | Generic MAVLink |
| `parameter_extraction.py` | All ArduPilot-based drones | Generic MAVLink |
| `packet_sniffing.py` | All ArduPilot-based drones | Generic MAVLink |
| `protocol_fingerprinting.py` | All ArduPilot-based drones | Generic MAVLink |
| `mavlink_mitm.py` | All ArduPilot-based drones | Generic MAVLink |
| `command_replay.py` | All ArduPilot-based drones | Generic MAVLink |
| `telemetry_replay.py` | All ArduPilot-based drones | Generic MAVLink |
| `firmware_extraction.py` | All ArduPilot-based drones | Generic MAVLink |
| `drone_discovery.py` | All ArduPilot-based drones | Generic MAVLink |
| `gcs_discovery.py` | All ArduPilot-based drones | Generic MAVLink |
| `gps_telemetry_tracking.py` | All ArduPilot-based drones | Generic MAVLink |

#### **DJI** (DJI Technology)
| Exploit | Model | CVE | Notes |
|---------|-------|-----|-------|
| `wifi_crack.py` | DJI Spark, Mavic Air, DJI Mini series | CVE-2025-10250 | WEP encryption |
| `wifi_crack.py` | Mavic 3 Series, Matrice 300, Mini 3 Pro | CVE-2023-6951 | WPA2 PSK weakness |
| `wifi_deauth.py` | All WiFi-enabled DJI drones | - | Generic WiFi attack |
| `wifi_client_data_leak.py` | All WiFi-enabled DJI drones | - | Generic WiFi attack |
| `camera_feed_eavesdropping.py` | DJI drones with RTSP streaming | - | Camera streaming |
| `drone_discovery.py` | All DJI drones | - | Network discovery |

#### **Holy Stone** (Holy Stone)
| Exploit | Model | CVE | Notes |
|---------|-------|-----|-------|
| `holy_stone_ble_rce_cve_2024_52876.py` | Holy Stone drones with HSRID01 Remote ID Module | CVE-2024-52876 | BLE RCE, Drone Go2 app < v1.1.8 |

#### **ExpressLRS Protocol** (Open Source FPV Community)
| Exploit | Model | Notes |
|---------|-------|-------|
| `expresslrs_uid_leakage.py` | FPV drones using ExpressLRS protocol | All ExpressLRS-compatible FPV drones |

#### **Parrot** (Parrot Drones SAS)
| Exploit | Model | Notes |
|---------|-------|-------|
| `wifi_deauth.py` | Parrot Bebop 2, Anafi | WiFi-enabled models |
| `wifi_client_data_leak.py` | Parrot Bebop 2, Anafi | WiFi-enabled models |
| `camera_feed_eavesdropping.py` | Parrot Bebop 2, Anafi | RTSP streaming |

#### **Generic/Protocol-Based** (Multiple Manufacturers)
| Exploit | Protocol/Technology | Applicable Models |
|---------|-------------------|-------------------|
| `web_ui_brute_force.py` | Companion Computer Web UI | Any drone with companion computer web interface |
| `companion_computer_exploit.py` | Companion Computer | Any drone with companion computer (Raspberry Pi, etc.) |
| `companion_computer_discovery.py` | Companion Computer | Any drone with companion computer |
| `ros_topic_flooding.py` | ROS (Robot Operating System) | ROS-based drones with companion computers |
| `camera_feed_eavesdropping.py` | RTSP Protocol | Any drone with RTSP camera streaming |
| `ftp_eavesdropping.py` | FTP Protocol | Any drone with FTP services |
| `arp_spoofing.py` | Network Protocol | Any network-connected drone |
| `dns_spoofing.py` | Network Protocol | Any network-connected drone |
| `firmware_analysis.py` | Firmware Analysis | All drone firmware types |
| `wireless_network_exploit.py` | Wireless Networks | Any drone capable of carrying payload (2026 research) |
| `data_interception.py` | Wireless Interception | Any drone with wireless interception capability |
| `physical_payload_delivery.py` | Physical Delivery | Any drone with payload delivery capability |
| `multi_vector_attack.py` | Multi-Vector | Any drone platform (coordinated attacks) |

### Summary by Manufacturer

| Manufacturer | Exploits Count | Primary Attack Vectors |
|--------------|----------------|----------------------|
| **PX4-Autopilot** | 35+ | Buffer overflows, RCE, Geofence bypass, MAVLink injection |
| **ArduPilot** | 30+ | MAVLink protocol exploits, GPS spoofing, Parameter manipulation |
| **DJI** | 6 | WiFi protocol exploitation (WEP/WPA2), Network attacks |
| **Holy Stone** | 1 | BLE RCE (CVE-2024-52876) |
| **ExpressLRS** | 1 | UID leakage, Binding phrase exploitation |
| **Parrot** | 3 | WiFi attacks, Camera feed interception |
| **Generic/Protocol** | 10+ | Protocol-based attacks (ROS, RTSP, FTP, Network) |

### Coverage Statistics

- **Total Manufacturers Covered**: 6+ (PX4, ArduPilot, DJI, Holy Stone, ExpressLRS, Parrot)
- **Total Exploit Scripts**: 73+
- **Protocol-Based Coverage**: MAVLink, WiFi, BLE, ExpressLRS, ROS, RTSP, FTP
- **CVE-Specific Exploits**: 10+ (targeting specific firmware versions)
- **Automated Attack Systems**: Hail Mary Attack (multi-vector automated exploitation)

---

## 🚀 Quick Start

### Prerequisites

- **Docker** and **Docker Compose** installed
- **Kali Linux** (recommended) or compatible Linux distribution
- **System Requirements**:
  - **Lite Mode**: 4-8 GB RAM, 2 CPU cores, 100 GB disk
  - **Full Mode**: 8-16 GB RAM, 2-4 CPU cores, 100 GB disk, GPU with 2GB+ VRAM

### 1-Minute Setup

```bash
# Navigate to simulator directory
cd "Drone Research/Damn-Vulnerable-Drone"

# Start in Lite Mode (no GPU required)
sudo ./start.sh --mode lite --no-wifi

# Access the interfaces
# Management Console: http://localhost:8000
# Companion Computer: http://localhost:3000
```

---

## 📦 Installation

### Step 1: Install Docker

**On Kali Linux:**
```bash
# Add Docker repository
printf '%s\n' "deb https://download.docker.com/linux/debian bullseye stable" | sudo tee /etc/apt/sources.list.d/docker-ce.list

# Import GPG key
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/docker-ce-archive-keyring.gpg

# Update and install
sudo apt update -y
sudo apt install docker-ce docker-ce-cli containerd.io -y

# Start Docker service
sudo systemctl enable docker --now

# Add user to docker group
sudo usermod -aG docker $USER
# Log out and back in for group changes to take effect
```

### Step 2: Clone Repository

```bash
git clone https://github.com/yourusername/damn-vulnerable-drone.git
cd damn-vulnerable-drone
```

### Step 3: Choose Your Mode

#### Lite Mode (Recommended for First Time)
```bash
sudo ./start.sh --mode lite --no-wifi
```

#### Full Mode (3D Environment)
```bash
sudo ./start.sh --mode full --no-wifi
```

#### With WiFi Simulation
```bash
# WEP encryption
sudo ./start.sh --mode lite --wifi wep

# WPA2 encryption
sudo ./start.sh --mode lite --wifi wpa2
```

For detailed installation instructions, see [SETUP_GUIDE.md](Damn-Vulnerable-Drone/SETUP_GUIDE.md).

---

## 📖 Usage Guide

### Accessing the Web Interfaces

1. **Management Console** (`http://localhost:8000`)
   - View attack scenarios
   - Execute exploits
   - Monitor system status
   - Track progress

2. **Companion Computer** (`http://localhost:3000`)
   - Web-based drone interface
   - Mission planning
   - Telemetry monitoring

### Running Exploits via Web Interface

1. Navigate to `http://localhost:8000`
2. Click on **"Attacks"** in the navigation menu
3. Browse available attack scenarios by category
4. Select a scenario and click **"Execute"**
5. Monitor execution status and results

### Running Exploits via Command Line

```bash
# Example: Buffer overflow attack
cd Damn-Vulnerable-Drone
python3 exploits/injection/buffer_overflow_cve_2024_40427.py udp:127.0.0.1:14550

# Example: GPS spoofing
python3 exploits/tampering/gps_spoofing.py udp:127.0.0.1:14550 37.7749 -122.4194 100

# Example: Flight log extraction
python3 exploits/exfiltration/flight_log_extraction.py udp:127.0.0.1:14550
```

### Using Attack Chains

```bash
# Execute a predefined attack chain
python3 exploits/chains/chain_executor.py chain_id

# View available chains
curl http://localhost:8000/api/exploits/chains
```

For comprehensive usage instructions, see [USAGE_GUIDE.md](Damn-Vulnerable-Drone/USAGE_GUIDE.md).

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Network (10.13.0.0/24)            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐  ┌──────────────────┐               │
│  │ Flight Controller│  │ Companion Computer│               │
│  │  (ArduPilot SITL)│  │   (Flask Web UI) │               │
│  │   10.13.0.2      │  │    10.13.0.3      │               │
│  │   Port: 14550    │  │   Port: 3000      │               │
│  └──────────────────┘  └──────────────────┘               │
│                                                              │
│  ┌──────────────────┐  ┌──────────────────┐               │
│  │ Ground Control   │  │   Simulator      │               │
│  │   Station        │  │  (Management)    │               │
│  │  (QGroundControl)│  │   (Flask API)    │               │
│  │   10.13.0.4      │  │    10.13.0.5      │               │
│  │                  │  │   Port: 8000     │               │
│  └──────────────────┘  └──────────────────┘               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Components

- **Flight Controller**: ArduPilot SITL simulation
- **Companion Computer**: Web interface and services
- **Ground Control Station**: QGroundControl integration
- **Simulator**: Management console and exploit execution

---

## 📚 Documentation

### Core Documentation

- **[SETUP_GUIDE.md](Damn-Vulnerable-Drone/SETUP_GUIDE.md)** - Detailed installation and configuration
- **[USAGE_GUIDE.md](Damn-Vulnerable-Drone/USAGE_GUIDE.md)** - Comprehensive usage instructions
- **[API_DOCUMENTATION.md](Damn-Vulnerable-Drone/API_DOCUMENTATION.md)** - REST API reference
- **[VULNERABILITIES_AND_EXPLOITS.md](Damn-Vulnerable-Drone/VULNERABILITIES_AND_EXPLOITS.md)** - Complete vulnerability analysis
- **[HARDWARE_REQUIREMENTS.md](Damn-Vulnerable-Drone/HARDWARE_REQUIREMENTS.md)** - Hardware setup guide

### Research Documentation

- **[RESEARCH.md](Damn-Vulnerable-Drone/RESEARCH.md)** - Comprehensive research document (14 sections)
- **[REPOSITORIES.md](Damn-Vulnerable-Drone/REPOSITORIES.md)** - GitHub repository catalog
- **[SUMMARY.md](Damn-Vulnerable-Drone/SUMMARY.md)** - Quick reference guide
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and updates

---

## 📊 Statistics

### Project Metrics

- **Exploit Scripts**: 73+
- **Attack Categories**: 11
- **Real-World CVEs**: 10+
- **Attack Scenarios**: 40+
- **Documented Vulnerabilities**: 46
- **Lines of Code**: 10,000+
- **Docker Containers**: 4
- **Web Interfaces**: 2

### CVE Coverage

| CVE | CVSS Score | Category | Status |
|-----|------------|----------|--------|
| CVE-2024-40427 | 7.9 | Buffer Overflow | ✅ Implemented |
| CVE-2024-38952 | 7.5 | Logger Overflow | ✅ Implemented |
| CVE-2024-38951 | 6.5 | Buffer Overflow | ✅ Implemented |
| CVE-2024-29460 | 6.6 | Flight Path Manipulation | ✅ Implemented |
| CVE-2024-30800 | - | Geofence Bypass | ✅ Implemented |
| CVE-2024-30799 | 4.4 | RCE | ✅ Implemented |
| CVE-2025-9020 | 4.5 | Use-After-Free | ✅ Implemented |
| CVE-2025-5640 | High | Trajectory Overflow | ✅ Implemented |
| CVE-2024-52876 | 7.5 | BLE RCE | ✅ Implemented |
| CVE-2024-24254 | 4.2 | Race Condition | ✅ Implemented |
| CVE-2024-24255 | 4.2 | Race Condition | ✅ Implemented |

---

## ⚠️ Legal Notice

**This project is for educational and authorized security research purposes only.**

### Important Legal Considerations

- ⚠️ Unauthorized access to or control of drones is **illegal** in most jurisdictions
- ✅ Only test on drones you own or have explicit written permission to test
- ✅ Follow responsible disclosure practices
- ✅ Comply with local aviation regulations
- ✅ Use in controlled, isolated environments
- ✅ Do not use these techniques on real-world systems without authorization

### Responsible Use

This platform is designed to:
- Educate security professionals
- Train security teams
- Conduct authorized security research
- Develop defensive strategies

**Misuse of this software is strictly prohibited and may result in legal consequences.**

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Follow code style** (PEP 8 for Python)
4. **Update documentation** (README, CHANGELOG, etc.)
5. **Test your changes** thoroughly
6. **Commit with clear messages** (`git commit -m 'Add amazing feature'`)
7. **Push to your branch** (`git push origin feature/amazing-feature`)
8. **Open a Pull Request**

### Contribution Areas

- New exploit scripts
- Documentation improvements
- Bug fixes
- Feature enhancements
- Test cases
- Security research

---

## 🔗 Resources

### Official Links

- **Original Project**: [Damn Vulnerable Drone](https://github.com/nicholasaleks/Damn-Vulnerable-Drone)
- **OWASP Top 10 Drone Security Risks**: [OWASP](https://owasp.org/www-project-top-10-drone-security-risks/)
- **MAVLink Protocol**: [MAVLink.io](https://mavlink.io/)
- **ArduPilot**: [ArduPilot.org](https://ardupilot.org/)

### Learning Resources

- [Drone Security Research Papers](Damn-Vulnerable-Drone/RESEARCH.md)
- [Vulnerability Database](Damn-Vulnerable-Drone/VULNERABILITIES_AND_EXPLOITS.md)
- [API Documentation](Damn-Vulnerable-Drone/API_DOCUMENTATION.md)

---

## 📝 Version History

**Current Version**: 1.1.0

See [CHANGELOG.md](CHANGELOG.md) for detailed version history and updates.

### Recent Updates

- ✅ 72+ exploit scripts implemented
- ✅ 10+ real-world CVE exploits
- ✅ Attack chain orchestration
- ✅ Web-based management console
- ✅ Comprehensive documentation

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](Damn-Vulnerable-Drone/LICENSE) file for details.

---

## 🌟 Star History

If you find this project useful, please consider giving it a ⭐ on GitHub!

---

**Last Updated**: January 22, 2026  
**Status**: Active Development & Research  
**Maintainer**: Security Research Team

---

<div align="center">

**Made with ❤️ for the security research community**

[⬆ Back to Top](#-damn-vulnerable-drone---professional-security-research-platform)

</div>
# Drone-hijack
