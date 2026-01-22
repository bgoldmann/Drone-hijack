# Quick Reference: Drone Hijacking Research Summary

> **Quick navigation guide** - For detailed information, see the full documentation files listed in README.md

## Critical Vulnerabilities at a Glance

### 🔴 DJI Enhanced Wi-Fi Protocol
- **CVE-2025-10250**: WEP encryption (recoverable in 20 seconds)
- **CVE-2023-6951**: Weak WPA2 PSK in QuickTransfer Mode
- **Affected**: DJI Mini SE, Spark, Mavic Air, Mini series, Mavic 3, Matrice 300
- **PoC**: [ibndias/dji-drone-hijacking](https://github.com/ibndias/dji-drone-hijacking)
- **Research**: arXiv:2309.05913

### 🔴 ExpressLRS Protocol
- **Issue**: MD5-based binding phrase, 75% UID leakage
- **Attack**: Brute force remaining 25% (1 byte)
- **Impact**: Full control takeover
- **Advisory**: NCC Group Technical Advisory
- **Status**: No fix implemented (encryption discussed but not added)

### 🔴 MAVLink/ArduPilot
- **CVE-2024-40427**: Stack buffer overflow (Severity: 7.9)
- **Multiple CVEs**: Buffer overflows, geofence bypass, race conditions
- **Educational**: [Damn Vulnerable Drone](https://github.com/nicholasaleks/Damn-Vulnerable-Drone)
- **Security Extension**: [MAVSec](https://github.com/aniskoubaa/mavsec)

---

## Top GitHub Repositories

| Repository | Purpose | Stars |
|------------|---------|-------|
| [ibndias/dji-drone-hijacking](https://github.com/ibndias/dji-drone-hijacking) | DJI PoC Exploit | - |
| [nicholasaleks/Damn-Vulnerable-Drone](https://github.com/nicholasaleks/Damn-Vulnerable-Drone) | Educational Simulator | 308+ |
| [rub-syssec/dronesecurity-fuzzer](https://github.com/rub-syssec/dronesecurity-fuzzer) | NDSS 2023 Fuzzer | - |
| [readloud/Drone-Hacking-Tool](https://github.com/readloud/Drone-Hacking-Tool) | GUI Tool | - |

---

## Attack Vectors

1. **Wi-Fi Protocol Exploitation**
   - WEP/WPA2 weaknesses
   - Control command interception
   - Packet manipulation

2. **Radio Control Attacks**
   - ExpressLRS UID leakage
   - Binding phrase exploitation

3. **MAVLink Exploits**
   - Buffer overflows
   - Command injection
   - Geofence bypass

4. **Physical Attacks**
   - GPS spoofing
   - Jamming
   - Camera tracking exploitation

---

## Key Academic Papers

- **arXiv:2309.05913** - DJI Enhanced Wi-Fi Protocol reverse engineering
- **arXiv:2403.03858v1** - Jamming and hijacking attacks
- **arXiv:2509.20362** - FlyTrap camera tracking attack
- **arXiv:2512.01164** - ArduPilot security analysis
- **NDSS 2023** - DroneSecurity Fuzzer research

---

## CVE Quick Reference

### DJI
- CVE-2025-10250 (WEP)
- CVE-2023-6951 (WPA2 PSK)

### PX4-Autopilot
- CVE-2024-40427 (Buffer overflow, 7.9)
- CVE-2024-38951, CVE-2024-38952 (Buffer overflows)
- CVE-2024-30800 (Geofence bypass)
- CVE-2024-24254, CVE-2024-24255 (Race conditions)
- CVE-2021-34125 (Unauthorized execution)

---

## Mitigation Quick Tips

### For Manufacturers
- Replace WEP with WPA3+
- Implement end-to-end encryption
- Add replay protection
- Regular security patches

### For Operators
- Keep firmware updated
- Use strong passwords
- Secure Wi-Fi networks
- Monitor for unauthorized access
- Enable geofencing

---

## Legal Warning

⚠️ **Unauthorized drone hijacking is illegal in most jurisdictions**

**Legitimate Use Only**:
- Own drones only
- Written authorization for testing
- Controlled environments
- Responsible disclosure

---

## 📚 Full Documentation

For comprehensive details, see:
- **README.md** - Complete project overview and structure
- **RESEARCH.md** - Comprehensive 14-section research document
- **VULNERABILITIES_AND_EXPLOITS.md** - Detailed vulnerability analysis (40 scenarios)
- **REPOSITORIES.md** - Detailed GitHub repository catalog
- **SETUP_GUIDE.md** - Installation and setup instructions
- **RECOMMENDATION.md** - Repository selection guide
- **CHANGELOG.md** - Version history and updates

---

**Last Updated**: January 22, 2026  
**Repository Version**: 1.3.1
