# GitHub Repository Catalog: Drone Hijacking & Security Research

## Primary Research Repositories

### 1. ibndias/dji-drone-hijacking
**URL**: https://github.com/ibndias/dji-drone-hijacking

**Description**: DJI Drone Control Hijacking - Proof of Concept

**Key Features**:
- Python scripts for drone control hijacking
- C code for router-based interception
- Targets DJI Mini SE drones
- Based on academic research (arXiv:2309.05913)

**Technology Stack**:
- Python (`drone.py`, `puppeteer.py`)
- C (`puppet.c`)
- Requires: Wi-Fi router with Ath9K chip, 5MHz monitor mode

**Use Case**: Proof-of-concept demonstration of DJI Enhanced Wi-Fi Protocol vulnerabilities

---

### 2. nicholasaleks/Damn-Vulnerable-Drone
**URL**: https://github.com/nicholasaleks/Damn-Vulnerable-Drone

**Description**: Intentionally vulnerable drone hacking simulator based on ArduPilot/MAVLink architecture

**Key Features**:
- 308+ GitHub stars
- Educational security testing environment
- Realistic ArduPilot/MAVLink architecture
- No physical hardware required
- Safe sandbox for learning

**Technology Stack**:
- ArduPilot framework
- MAVLink protocol
- Simulator-based

**Use Case**: Educational tool for offensive security training and penetration testing

---

### 3. RUB-SysSec/DroneSecurity-Fuzzer
**URL**: https://github.com/rub-syssec/dronesecurity-fuzzer

**Description**: DroneSecurity Fuzzer (NDSS 2023)

**Key Features**:
- Black-box fuzzing for DJI drones
- DJI DUML protocol analysis
- No source code or firmware access required
- Research presented at NDSS 2023

**Technology Stack**:
- Fuzzing framework
- USB protocol analysis
- DJI DUML protocol

**Use Case**: Automated vulnerability discovery in DJI drone protocols

---

### 4. aniskoubaa/mavsec
**URL**: https://github.com/aniskoubaa/mavsec

**Description**: Security extensions to MAVLink 2.0 protocol

**Key Features**:
- Encryption schemes: RC4, AES-CBC, AES-CTR, ChaCha20
- MAVLink 2.0 security enhancements
- ArduPilot/PX4 support

**Technology Stack**:
- MAVLink 2.0
- Multiple encryption algorithms
- C/C++ implementation

**Use Case**: Security research and implementation for MAVLink protocol

---

## Tool Repositories

### 5. readloud/Drone-Hacking-Tool
**URL**: https://github.com/readloud/Drone-Hacking-Tool

**Description**: GUI tool for hacking drones using USB Wi-Fi adapter and HackRF One

**Key Features**:
- GUI-based interface
- USB Wi-Fi adapter support
- HackRF One SDR integration
- Tested with DJI Tello and Parrot Bebop 2
- Wi-Fi deauthentication attacks
- GPS spoofing capabilities

**Technology Stack**:
- Aircrack-ng suite
- HackRF One
- USB Wi-Fi adapters
- GUI framework

**Use Case**: Practical drone security testing and research

---

### 6. HKSSY/Drone-Hacking-Tool
**URL**: https://github.com/HKSSY/Drone-Hacking-Tool

**Description**: Similar to readloud/Drone-Hacking-Tool

**Key Features**:
- GUI-based drone hacking tool
- Wi-Fi and SDR-based attacks
- Multiple drone model support

**Use Case**: Alternative implementation of drone hacking tools

---

### 7. ANG13T/drone-hacking-workshop
**URL**: https://github.com/ANG13T/drone-hacking-workshop

**Description**: Files and Programs for Drone Hacking Workshop

**Key Features**:
- Workshop materials and labs
- Port exploit exercises
- Wi-Fi packet analysis
- Digital forensics exercises

**Technology Stack**:
- Various security tools
- Network analysis tools
- Forensics tools

**Use Case**: Educational workshop materials for drone security

---

## Analysis & Research Repositories

### 8. ByteMe1001/DJI-Enhanced-WiFi-Weak-Cryptography
**URL**: https://github.com/ByteMe1001/DJI-Enhanced-WiFi-Weak-Cryptography

**Description**: Analysis of weak cryptography in DJI Enhanced Wi-Fi Protocol

**Key Features**:
- Detailed cryptographic analysis
- WEP encryption weaknesses
- Security research documentation

**Use Case**: Cryptographic security research on DJI protocols

---

## Repository Statistics Summary

| Repository | Primary Focus | Language | Stars | Active |
|------------|---------------|----------|-------|--------|
| ibndias/dji-drone-hijacking | PoC Exploit | Python, C | - | Research |
| nicholasaleks/Damn-Vulnerable-Drone | Educational | Various | 308+ | Active |
| rub-syssec/dronesecurity-fuzzer | Fuzzing | Various | - | Research |
| aniskoubaa/mavsec | Security Extension | C/C++ | - | Research |
| readloud/Drone-Hacking-Tool | GUI Tool | Various | - | Active |
| HKSSY/Drone-Hacking-Tool | GUI Tool | Various | - | Active |
| ANG13T/drone-hacking-workshop | Education | Various | - | Workshop |
| ByteMe1001/DJI-Enhanced-WiFi-Weak-Cryptography | Analysis | Various | - | Research |

---

## Target Drone Models

### DJI Drones
- DJI Mini SE
- DJI Spark
- DJI Mavic Air
- DJI Mini series
- DJI Mavic 3 Series
- DJI Matrice 300
- DJI Mini 3 Pro
- DJI Tello

### Other Brands
- Parrot Bebop 2
- HoverAir drones
- Generic MAVLink/ArduPilot drones

---

## Attack Vectors Covered

1. **Wi-Fi Protocol Exploitation**
   - WEP encryption cracking
   - WPA2 PSK weaknesses
   - Control command interception
   - Packet manipulation

2. **Radio Control Protocol Attacks**
   - ExpressLRS vulnerabilities
   - Binding phrase exploitation
   - UID leakage attacks

3. **MAVLink Protocol Exploits**
   - Buffer overflow attacks
   - Command injection
   - Geofence bypass
   - Mission planning vulnerabilities

4. **Physical Attacks**
   - GPS spoofing
   - Jamming attacks
   - Camera-based tracking exploitation

---

## Legal and Ethical Notes

⚠️ **Important**: All repositories listed are for educational and authorized security research purposes only. Unauthorized use of these tools against drones you do not own or have explicit permission to test is illegal in most jurisdictions.

**Responsible Use**:
- Only test on drones you own
- Obtain written authorization for penetration testing
- Follow responsible disclosure practices
- Comply with local aviation regulations
- Use in controlled, isolated environments

---

## Research Connections

### Academic Papers
- arXiv:2309.05913 - Directly related to ibndias/dji-drone-hijacking
- NDSS 2023 - Related to rub-syssec/dronesecurity-fuzzer
- Multiple other papers referenced in RESEARCH.md

### Security Advisories
- CVE-2025-10250 - DJI WEP vulnerability
- CVE-2023-6951 - DJI WPA2 PSK vulnerability
- NCC Group ExpressLRS Advisory
- Multiple PX4-Autopilot CVEs

---

---

**Last Updated**: January 22, 2026  
**Repository Version**: 1.3.1  
**Catalog Version**: 1.0

For related documentation, see:
- **README.md** - Project overview and structure
- **RESEARCH.md** - Comprehensive research document
- **RECOMMENDATION.md** - Repository selection guide
- **CHANGELOG.md** - Version history
