# Deep Research: Drone Hijacking on GitHub

## Executive Summary

This document provides comprehensive research on drone hijacking vulnerabilities, focusing on GitHub repositories, academic research, and real-world security exploits. The research reveals critical vulnerabilities across multiple drone communication protocols and platforms.

---

## 1. DJI Enhanced Wi-Fi Protocol Vulnerabilities

### 1.1 Primary Repository: ibndias/dji-drone-hijacking

**Repository**: [ibndias/dji-drone-hijacking](https://github.com/ibndias/dji-drone-hijacking)

**Description**: Proof-of-concept repository demonstrating hijacking of DJI Mini SE drones through reverse engineering of DJI's Enhanced Wi-Fi Protocol.

**Key Components**:
- Python scripts (`drone.py`, `puppeteer.py`)
- C code (`puppet.c`)
- Router-based interception system

**Technical Requirements**:
- Wi-Fi router with Ath9K chip support
- 5MHz monitor mode capability
- Commercial off-the-shelf equipment

**Attack Vector**: Intercepts and manipulates control commands between controller and drone through Wi-Fi protocol exploitation.

### 1.2 Academic Research Foundation

**Paper**: "Behind The Wings: The Case of Reverse Engineering and Drone Hijacking in DJI Enhanced Wi-Fi Protocol"
- **arXiv ID**: 2309.05913
- **Publication Date**: September 12, 2023
- **Authors**: Derry Pratama, Jaegeun Moon, Agus Mahardika Ari Laksmono, Dongwook Yun, Iqbal Muhammad, Byeonguk Jeong, Janghyun Ji, and Howon Kim

**Key Findings**:
- Demonstrated successful hijacking of DJI Mini SE drone
- Control commands lack sufficient cryptographic protection
- Vulnerable to interception and manipulation
- Consumer drones increasingly weaponized in military contexts
- Urgent need for improved security protocols

### 1.3 CVE-2025-10250: WEP Encryption Weakness

**Vulnerability Details**:
- **Affected Models**: DJI Spark, Mavic Air, DJI Mini series
- **Encryption**: Wired Equivalent Privacy (WEP) - fundamentally insecure
- **Exploitation Time**: Encryption keys recoverable within 20 seconds using Aircrack-ng PTW attacks
- **Key Issues**:
  - Static keys remain unchanged across flights
  - No replay protection
  - Weak encryption standard (deprecated since 2004)

**Attack Capabilities**:
- Recover encryption keys in seconds
- Intercept UDP payloads carrying flight control commands
- Manipulate telemetry data
- Full control hijacking

### 1.4 CVE-2023-6951: WPA2 PSK Weakness

**Vulnerability Details**:
- **Affected Models**: Mavic 3 Series, Matrice 300, Mini 3 Pro
- **Issue**: Weak WPA2 PSK key generation in QuickTransfer Mode
- **Impact**: Unauthorized Wi-Fi network access and potential data exfiltration
- **Status**: DJI addressed 7 of 9 identified vulnerabilities through firmware updates

---

## 2. ExpressLRS Protocol Vulnerabilities

### 2.1 Overview

ExpressLRS is a popular open-source radio control protocol for FPV (First Person View) drones, widely used in the drone racing and hobbyist communities.

### 2.2 Security Vulnerabilities

**Technical Advisory**: NCC Group Research Blog
- **Binding Phrase System**: Uses MD5 hash to create Unique Identifier (UID)
- **Intended Purpose**: Anti-collision, not security

**Critical Weaknesses**:

1. **UID Leakage (75% exposure)**
   - Sync packets leak final three bytes of UID
   - Only one byte remains unknown
   - Brute forceable within feasible time

2. **Weak CRC Initialization**
   - Last two bytes of UID initialize CRC checks
   - Trivial packet verification

3. **FHSS Sequence Weakness**
   - Frequency hopping spread spectrum sequence generation flawed
   - 256 possible values reduce to only 128 unique sequences
   - Simplifies attack complexity

### 2.3 Attack Requirements

- Standard ExpressLRS-compatible transmitter
- Ability to observe traffic between legitimate transmitter and receiver
- Basic packet analysis tools

### 2.4 Attack Impact

Once UID is determined:
- Full connection to target aircraft
- Complete control takeover
- Potential crash if drone already airborne
- No authentication or encryption barriers

### 2.5 Security Status

- GitHub Discussion #1609: Encryption improvements discussed but unimplemented
- Binding phrase never intended for security
- Community awareness but no immediate fix

---

## 3. MAVLink/ArduPilot Security Vulnerabilities

### 3.1 Damn Vulnerable Drone

**Repository**: [nicholasaleks/Damn-Vulnerable-Drone](https://github.com/nicholasaleks/Damn-Vulnerable-Drone)

**Description**: Intentionally vulnerable drone simulator based on ArduPilot/MAVLink architecture for educational security testing.

**Features**:
- 308+ GitHub stars
- Cost-free hands-on environment
- Realistic ArduPilot/MAVLink architecture
- Safe sandbox for learning drone hacking
- No physical hardware required

**Use Cases**:
- Offensive security training
- Penetration testing education
- Security research
- Vulnerability demonstration

### 3.2 MAVSec Repository

**Repository**: [aniskoubaa/mavsec](https://github.com/aniskoubaa/mavsec)

**Description**: Security extensions to MAVLink 2.0 protocol.

**Security Implementations**:
- RC4 encryption
- AES-CBC encryption
- AES-CTR encryption
- ChaCha20 encryption
- ArduPilot/PX4 unmanned systems support

### 3.3 Critical CVEs in PX4-Autopilot

**CVE-2024-40427** (High Severity: 7.9)
- Stack buffer overflow in PX4-Autopilot v1.14.3
- Allows command execution and program crashes
- Affects `mavlink_receiver.cpp`

**CVE-2024-38951 & CVE-2024-38952**
- Buffer overflows via malformed MAVLink messages
- Denial of service vulnerabilities

**CVE-2024-30800**
- Geofence bypass vulnerability
- Allows unauthorized flight in restricted areas

**CVE-2024-24254 & CVE-2024-24255**
- Race conditions in mission planning
- Potential for unauthorized command execution

**CVE-2021-34125**
- Unauthorized command execution vulnerability
- Older but still relevant

### 3.4 Reverse Engineering Research

**Paper**: "Reverse Engineering and Control-Aware Security Analysis of the ArduPilot UAV Framework"
- **arXiv ID**: 2512.01164
- Comprehensive security analysis of ArduPilot framework
- Control-aware vulnerability assessment

---

## 4. Additional Drone Security Tools and Repositories

### 4.1 DroneSecurity Fuzzer

**Repository**: [RUB-SysSec/DroneSecurity-Fuzzer](https://github.com/rub-syssec/dronesecurity-fuzzer)

**Description**: Black-box fuzzer for DJI drones presented at NDSS 2023.

**Capabilities**:
- Generates inputs based on DJI DUML protocol over USB
- No source code or firmware access required
- Discovers security vulnerabilities through fuzzing
- Examines DJI's DroneID implementation

**Research Context**: NDSS 2023 (Network and Distributed System Security Symposium)

### 4.2 Drone Hacking Tools

**Repositories**:
- [readloud/Drone-Hacking-Tool](https://github.com/readloud/Drone-Hacking-Tool)
- [HKSSY/Drone-Hacking-Tool](https://github.com/HKSSY/Drone-Hacking-Tool)

**Features**:
- GUI-based tools
- USB Wi-Fi adapter support
- HackRF One software-defined radio integration
- Tested with DJI Tello and Parrot Bebop 2
- Wi-Fi deauthentication attacks
- GPS spoofing capabilities
- Aircrack-ng suite integration

### 4.3 Drone Hacking Workshop

**Repository**: [ANG13T/drone-hacking-workshop](https://github.com/ANG13T/drone-hacking-workshop)

**Contents**:
- Workshop files and programs
- Labs covering port exploits
- Wi-Fi packet analysis
- Digital forensics exercises
- Educational materials

### 4.4 DJI Enhanced WiFi Weak Cryptography

**Repository**: [ByteMe1001/DJI-Enhanced-WiFi-Weak-Cryptography](https://github.com/ByteMe1001/DJI-Enhanced-WiFi-Weak-Cryptography)

**Focus**: Detailed analysis of weak cryptography in DJI Enhanced Wi-Fi protocol.

---

## 5. Advanced Attack Vectors

### 5.1 FlyTrap Attack Framework

**Research**: "FlyTrap: Physical Distance-Pulling Attack Towards Camera-based Autonomous Target Tracking Systems"
- **arXiv ID**: 2509.20362
- **Target**: Camera-based autonomous target tracking systems
- **Affected Drones**: Commercial DJI and HoverAir drones
- **Method**: Physical-world attacks on tracking systems
- **Impact**: Successfully reduces tracking distances

### 5.2 ACAS-Xu System Exploitation

**Research**: "Hijacking an autonomous delivery drone equipped with the ACAS-Xu system"
- **Focus**: Exploitation of collision avoidance systems
- **Method**: System-specific vulnerabilities in ACAS-Xu implementation

### 5.3 Jamming and Hijacking Attacks

**Research**: "Exploring Jamming and Hijacking Attacks for Micro Aerial Drones"
- **arXiv ID**: 2403.03858v1
- Comprehensive analysis of jamming and hijacking techniques
- Micro aerial drone specific vulnerabilities

---

## 6. Industry and Academic Response

### 6.1 Counter-Drone Systems

**Ondas Holdings Inc. - Iron Drone Raider**
- Military-grade counter-drone system
- Designed to intercept hostile drones
- Protects borders, critical locations, and people
- Active deployment in military contexts

### 6.2 DroneTrace Platform

**Company**: DroneTrace
- AI-driven tactical exploitation platform
- Founded by veteran defense technology entrepreneurs
- Focus: Extracting intelligence from captured drones
- On-site exploitation capabilities
- UxS (Unmanned Systems) intelligence extraction

### 6.3 Academic Research Trends

**Recent Publications**:
- Multiple papers on drone security (2023-2024)
- Focus on protocol vulnerabilities
- Reverse engineering methodologies
- Real-world exploitability demonstrations

**Research Institutions**:
- Various universities and security research labs
- Industry partnerships with security firms
- Government-funded research projects

---

## 7. Legal and Ethical Considerations

### 7.1 Legal Status

⚠️ **Critical Warning**: Unauthorized access to or control of drones is illegal in most jurisdictions, including:
- United States (Federal Aviation Administration regulations)
- European Union (EASA regulations)
- Most countries with drone regulations

**Potential Legal Consequences**:
- Criminal charges for unauthorized access
- Violation of aviation regulations
- Potential terrorism-related charges
- Civil liability for damages

### 7.2 Ethical Use

**Legitimate Use Cases**:
- Security research with proper authorization
- Educational purposes in controlled environments
- Penetration testing with written consent
- Academic research with ethical review board approval

**Responsible Disclosure**:
- Report vulnerabilities to manufacturers
- Follow coordinated disclosure practices
- Allow time for patches before public disclosure
- Provide proof-of-concept only to authorized parties

---

## 8. Mitigation Strategies

### 8.1 For Drone Manufacturers

1. **Encryption Standards**
   - Replace WEP with WPA3 or stronger protocols
   - Implement end-to-end encryption
   - Use strong key exchange mechanisms

2. **Authentication**
   - Multi-factor authentication for control links
   - Certificate-based authentication
   - Regular key rotation

3. **Protocol Security**
   - Implement replay protection
   - Add message authentication codes (MACs)
   - Use secure random number generators

4. **Firmware Updates**
   - Regular security patches
   - Over-the-air update mechanisms
   - Vulnerability response programs

### 8.2 For Drone Operators

1. **Best Practices**
   - Keep firmware updated
   - Use strong, unique passwords
   - Enable all available security features
   - Monitor for unauthorized access

2. **Network Security**
   - Use secure Wi-Fi networks
   - Avoid public Wi-Fi for drone control
   - Implement network segmentation
   - Monitor network traffic

3. **Physical Security**
   - Secure storage when not in use
   - Limit access to authorized personnel
   - Use geofencing appropriately
   - Monitor flight logs

---

## 9. Future Research Directions

### 9.1 Emerging Threats

- AI-powered attack automation
- Machine learning-based protocol analysis
- Quantum computing implications
- 5G/6G network vulnerabilities

### 9.2 Defense Mechanisms

- Blockchain-based authentication
- AI-powered anomaly detection
- Hardware security modules
- Zero-trust architectures

### 9.3 Regulatory Evolution

- International drone security standards
- Mandatory security certifications
- Incident reporting requirements
- Liability frameworks

---

## 10. Repository Catalog

### 10.1 Primary Research Repositories

| Repository | Stars | Focus | Language |
|------------|-------|-------|----------|
| ibndias/dji-drone-hijacking | - | DJI PoC | Python, C |
| nicholasaleks/Damn-Vulnerable-Drone | 308+ | Educational | Various |
| rub-syssec/dronesecurity-fuzzer | - | Fuzzing | Various |
| aniskoubaa/mavsec | - | MAVLink Security | Various |
| ByteMe1001/DJI-Enhanced-WiFi-Weak-Cryptography | - | Crypto Analysis | Various |

### 10.2 Tool Repositories

| Repository | Focus | Hardware |
|------------|-------|----------|
| readloud/Drone-Hacking-Tool | GUI Tool | USB Wi-Fi, HackRF One |
| HKSSY/Drone-Hacking-Tool | GUI Tool | USB Wi-Fi, HackRF One |
| ANG13T/drone-hacking-workshop | Workshop | Various |

---

## 11. Academic Papers Reference

1. **arXiv:2309.05913** - "Behind The Wings: The Case of Reverse Engineering and Drone Hijacking in DJI Enhanced Wi-Fi Protocol" (2023)

2. **arXiv:2403.03858v1** - "Exploring Jamming and Hijacking Attacks for Micro Aerial Drones" (2024)

3. **arXiv:2509.20362** - "FlyTrap: Physical Distance-Pulling Attack Towards Camera-based Autonomous Target Tracking Systems" (2025)

4. **arXiv:2512.01164** - "Reverse Engineering and Control-Aware Security Analysis of the ArduPilot UAV Framework" (2025)

5. **arXiv:2512.03792** - "Unfolding Challenges in Securing and Regulating Unmanned Air..." (2025)

6. **NDSS 2023** - DroneSecurity Fuzzer research presentation

7. **HAL Science** - "Hijacking an autonomous delivery drone equipped with the ACAS-Xu system"

---

## 12. CVE Reference List

### DJI Vulnerabilities
- **CVE-2025-10250**: WEP encryption weakness in Enhanced Wi-Fi Protocol
- **CVE-2023-6951**: Weak WPA2 PSK in QuickTransfer Mode

### PX4-Autopilot Vulnerabilities
- **CVE-2024-40427**: Stack buffer overflow (High: 7.9)
- **CVE-2024-38951**: Buffer overflow via malformed MAVLink
- **CVE-2024-38952**: Buffer overflow via malformed MAVLink
- **CVE-2024-30800**: Geofence bypass
- **CVE-2024-24254**: Race condition in mission planning
- **CVE-2024-24255**: Race condition in mission planning
- **CVE-2021-34125**: Unauthorized command execution

### ExpressLRS
- **NCC Group Advisory**: MD5-based binding phrase vulnerabilities (No CVE assigned as of research date)

---

## 13. Conclusion

This research reveals significant security vulnerabilities across multiple drone platforms and communication protocols. The availability of proof-of-concept exploits on GitHub, combined with academic research demonstrating real-world exploitability, highlights the urgent need for:

1. **Improved Security Standards**: Replacement of deprecated encryption protocols
2. **Better Authentication**: Multi-factor and certificate-based systems
3. **Regular Updates**: Timely firmware patches and security updates
4. **Education**: Awareness of vulnerabilities and mitigation strategies
5. **Regulation**: International standards for drone security

The open-source nature of many exploits and tools provides both opportunities for security research and risks of malicious use. Responsible disclosure and ethical research practices are essential.

---

## 14. References and Links

### GitHub Repositories
- https://github.com/ibndias/dji-drone-hijacking
- https://github.com/nicholasaleks/Damn-Vulnerable-Drone
- https://github.com/rub-syssec/dronesecurity-fuzzer
- https://github.com/aniskoubaa/mavsec
- https://github.com/readloud/Drone-Hacking-Tool
- https://github.com/HKSSY/Drone-Hacking-Tool
- https://github.com/ANG13T/drone-hacking-workshop
- https://github.com/ByteMe1001/DJI-Enhanced-WiFi-Weak-Cryptography

### Academic Papers
- https://arxiv.org/abs/2309.05913
- https://arxiv.org/pdf/2309.05913
- https://arxiv.org/html/2403.03858v1
- https://arxiv.org/abs/2509.20362
- https://www.arxiv.org/pdf/2512.01164

### Security Advisories
- https://www.nccgroup.com/research-blog/technical-advisory-expresslrs-vulnerabilities-allow-for-hijack-of-control-link/
- https://nvd.nist.gov/vuln/detail/CVE-2023-6951
- https://github.com/PX4/PX4-Autopilot/security/advisories/GHSA-55wq-2hgm-75m4

### Industry Resources
- https://www.dronetrace.com/
- https://cuashub.com/en/content/reverse-engineering-and-hijacking-dji-enhanced-wi-fi-protocol/
- https://threatpost.com/drone-hack-expresslrs-hijacked/180133/

---

---

**Research Compiled**: January 22, 2026  
**Last Updated**: January 22, 2026  
**Repository Version**: 1.3.1  
**Status**: Active Research

For related documentation, see:
- **README.md** - Project overview and structure
- **VULNERABILITIES_AND_EXPLOITS.md** - Detailed vulnerability analysis
- **SUMMARY.md** - Quick reference guide
- **CHANGELOG.md** - Version history
