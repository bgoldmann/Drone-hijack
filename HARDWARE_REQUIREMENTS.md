# Hardware Requirements Guide

This document outlines the hardware requirements for running the Damn Vulnerable Drone simulator and executing various exploit scripts. While the simulator itself runs in a virtualized Docker environment, certain exploits require specific hardware for realistic attack scenarios.

## Table of Contents

- [Basic System Requirements](#basic-system-requirements)
- [WiFi Attacks Hardware](#wifi-attacks-hardware)
- [SDR/Radio Attacks Hardware](#sdrradio-attacks-hardware)
- [Network Attacks Hardware](#network-attacks-hardware)
- [Camera/Streaming Hardware](#camerastreaming-hardware)
- [Exploit-Specific Hardware Requirements](#exploit-specific-hardware-requirements)
- [Recommended Hardware Kits](#recommended-hardware-kits)
- [Hardware Setup Instructions](#hardware-setup-instructions)

---

## Basic System Requirements

### Minimum Requirements (Lite Mode)
- **CPU**: 2 cores (x86_64)
- **RAM**: 4-8 GB
- **Storage**: 100 GB free space
- **OS**: Kali Linux (recommended) or compatible Linux distribution
- **Network**: Ethernet or WiFi adapter

### Recommended Requirements (Full Mode)
- **CPU**: 2-4 cores (x86_64)
- **RAM**: 8-16 GB
- **Storage**: 100 GB free space
- **GPU**: 2GB+ VRAM (for Gazebo 3D simulator)
- **OS**: Kali Linux (bare metal recommended)
- **Network**: Ethernet or WiFi adapter

---

## WiFi Attacks Hardware

### WiFi Dongles for Monitor Mode

Many wireless attacks require a WiFi adapter that supports **monitor mode** and **packet injection**. The simulator uses virtual WiFi interfaces, but for real-world testing, you'll need compatible hardware.

#### Recommended WiFi Adapters

1. **Alfa AWUS036ACH** (Best Overall)
   - **Chipset**: Realtek RTL8812AU
   - **Frequency**: 2.4 GHz & 5 GHz dual-band
   - **Features**: 
     - Monitor mode support
     - Packet injection
     - High power (1000mW)
   - **Price**: ~$50-70
   - **Compatibility**: Excellent with Kali Linux
   - **Use Cases**: 
     - `exploits/recon/wifi_crack.py`
     - `exploits/dos/wifi_deauth.py`
     - `exploits/recon/packet_sniffing.py`

2. **Alfa AWUS036NHA**
   - **Chipset**: Atheros AR9271
   - **Frequency**: 2.4 GHz only
   - **Features**: 
     - Monitor mode support
     - Packet injection
     - High power (1000mW)
   - **Price**: ~$30-40
   - **Compatibility**: Excellent with Kali Linux
   - **Use Cases**: 2.4 GHz WiFi attacks

3. **TP-Link TL-WN722N v1** (Budget Option)
   - **Chipset**: Atheros AR9271
   - **Frequency**: 2.4 GHz
   - **Features**: 
     - Monitor mode support
     - Packet injection
   - **Price**: ~$15-20
   - **Note**: Only v1 works (v2/v3 use different chipsets)
   - **Use Cases**: Basic WiFi attacks

4. **Pineapple WiFi Adapter**
   - **Chipset**: Various (check compatibility)
   - **Frequency**: 2.4 GHz & 5 GHz
   - **Features**: 
     - Designed for penetration testing
     - Monitor mode support
   - **Price**: ~$40-60

#### WiFi Adapter Requirements Checklist

✅ **Must Support**:
- Monitor mode (`iwconfig wlan0 mode monitor`)
- Packet injection (for deauth attacks)
- Promiscuous mode
- 802.11 a/b/g/n/ac standards

✅ **Recommended Features**:
- External antenna connector
- High transmit power (500mW+)
- USB 3.0 support
- Linux kernel driver support

#### Exploits Requiring WiFi Adapter

| Exploit Script | WiFi Adapter Required | Notes |
|---------------|----------------------|-------|
| `recon/wifi_crack.py` | ✅ Yes | WEP/WPA2 cracking |
| `dos/wifi_deauth.py` | ✅ Yes | Deauthentication attacks |
| `recon/packet_sniffing.py` | ✅ Yes | MAVLink traffic capture |
| `network/arp_spoofing.py` | ⚠️ Optional | Works with Ethernet too |
| `exfiltration/camera_feed_eavesdropping.py` | ❌ No | Uses RTSP over network |

---

## SDR/Radio Attacks Hardware

### Software-Defined Radio (SDR) Devices

For radio frequency attacks, GPS spoofing, and ExpressLRS protocol attacks, you'll need an SDR device.

#### HackRF One (Recommended)

- **Manufacturer**: Great Scott Gadgets
- **Frequency Range**: 1 MHz - 6 GHz
- **Sample Rate**: Up to 20 MS/s
- **Price**: ~$100-150
- **Features**:
  - Half-duplex (transmit or receive, not both simultaneously)
  - 8-bit ADC
  - USB 3.0 interface
  - Open source hardware
- **Use Cases**:
  - `injection/expresslrs_uid_leakage.py` - ExpressLRS protocol attacks
  - GPS spoofing (with additional software)
  - Radio frequency analysis
  - Signal replay attacks

#### Alternative SDR Devices

1. **BladeRF 2.0 Micro**
   - **Frequency Range**: 47 MHz - 6 GHz
   - **Price**: ~$200-300
   - **Features**: Full-duplex, higher performance
   - **Use Cases**: Advanced RF attacks

2. **RTL-SDR v3** (Budget Option)
   - **Frequency Range**: 24 MHz - 1.766 GHz
   - **Price**: ~$25-35
   - **Features**: Receive-only, USB 2.0
   - **Limitations**: Cannot transmit (receive only)
   - **Use Cases**: Signal analysis, monitoring

3. **LimeSDR Mini**
   - **Frequency Range**: 10 MHz - 3.5 GHz
   - **Price**: ~$150-200
   - **Features**: Full-duplex, higher bandwidth
   - **Use Cases**: Advanced RF research

#### Exploits Requiring SDR

| Exploit Script | SDR Required | Recommended Device |
|---------------|--------------|-------------------|
| `injection/expresslrs_uid_leakage.py` | ✅ Yes | HackRF One |
| `tampering/gps_spoofing.py` | ⚠️ Optional | HackRF One (for RF GPS spoofing) |
| `replay/command_replay.py` | ❌ No | Uses network capture |

**Note**: The simulator's GPS spoofing script works via MAVLink injection and doesn't require SDR. Real-world GPS spoofing via RF requires HackRF One or similar.

---

## Network Attacks Hardware

### Ethernet Adapters

For network-based attacks like ARP spoofing and MITM, standard network adapters work fine.

#### Requirements

- **Ethernet Adapter**: Any standard USB or built-in Ethernet adapter
- **Features Needed**:
  - Promiscuous mode support
  - Packet capture capability
- **Use Cases**:
  - `network/arp_spoofing.py`
  - `network/dns_spoofing.py`
  - `mitm/mavlink_mitm.py`

#### USB Ethernet Adapters (Optional)

If your system lacks Ethernet ports:
- **Any USB 3.0 to Ethernet adapter** (~$10-20)
- Works with most Linux distributions

---

## Camera/Streaming Hardware

### RTSP Streaming

The simulator includes RTSP camera streaming, but for real-world testing:

#### Requirements

- **Camera**: Any IP camera or USB webcam with RTSP support
- **Network**: WiFi or Ethernet connection
- **Software**: VLC, ffmpeg, or OpenCV
- **Use Cases**:
  - `exfiltration/camera_feed_eavesdropping.py`

#### Recommended Cameras

1. **USB Webcams** (Simple)
   - Logitech C920/C930e
   - Any UVC-compatible webcam
   - Price: ~$50-100

2. **IP Cameras** (Advanced)
   - Any ONVIF-compatible IP camera
   - Supports RTSP streaming
   - Price: ~$50-200

---

## Exploit-Specific Hardware Requirements

### Complete Hardware Matrix

| Exploit Category | Script | WiFi | SDR | Ethernet | Camera | Notes |
|----------------|--------|------|-----|----------|--------|-------|
| **Reconnaissance** |
| | `wifi_crack.py` | ✅ Required | ❌ | ❌ | ❌ | WEP/WPA2 cracking |
| | `drone_discovery.py` | ⚠️ Optional | ❌ | ✅ | ❌ | Network scanning |
| | `packet_sniffing.py` | ✅ Recommended | ❌ | ✅ | ❌ | Traffic capture |
| | `protocol_fingerprinting.py` | ❌ | ❌ | ✅ | ❌ | MAVLink analysis |
| | `gps_telemetry_tracking.py` | ❌ | ❌ | ✅ | ❌ | GPS data extraction |
| **Injection** |
| | `mavlink_inject.py` | ❌ | ❌ | ✅ | ❌ | Network-based |
| | `waypoint_override.py` | ❌ | ❌ | ✅ | ❌ | Network-based |
| | `parameter_manipulation.py` | ❌ | ❌ | ✅ | ❌ | Network-based |
| | `buffer_overflow_cve_2024_40427.py` | ❌ | ❌ | ✅ | ❌ | Network-based |
| | `expresslrs_uid_leakage.py` | ❌ | ✅ HackRF | ❌ | ❌ | RF protocol attack |
| | `mission_race_condition.py` | ❌ | ❌ | ✅ | ❌ | Network-based |
| | `geofence_bypass.py` | ❌ | ❌ | ✅ | ❌ | Network-based |
| | `return_to_home_override.py` | ❌ | ❌ | ✅ | ❌ | Network-based |
| **DoS** |
| | `wifi_deauth.py` | ✅ Required | ❌ | ❌ | ❌ | WiFi deauth attack |
| | `communication_flooding.py` | ❌ | ❌ | ✅ | ❌ | Network flooding |
| | `geofence_attack.py` | ❌ | ❌ | ✅ | ❌ | Network-based |
| | `flight_termination.py` | ❌ | ❌ | ✅ | ❌ | Network-based |
| **Exfiltration** |
| | `flight_log_extraction.py` | ❌ | ❌ | ✅ | ❌ | MAVLink-based |
| | `mission_extraction.py` | ❌ | ❌ | ✅ | ❌ | MAVLink-based |
| | `parameter_extraction.py` | ❌ | ❌ | ✅ | ❌ | MAVLink-based |
| | `camera_feed_eavesdropping.py` | ⚠️ Optional | ❌ | ✅ | ✅ | RTSP streaming |
| **Tampering** |
| | `gps_spoofing.py` | ❌ | ⚠️ Optional | ✅ | ❌ | MAVLink or RF |
| | `battery_spoofing.py` | ❌ | ❌ | ✅ | ❌ | MAVLink-based |
| | `attitude_spoofing.py` | ❌ | ❌ | ✅ | ❌ | MAVLink-based |
| | `sensor_data_injection.py` | ❌ | ❌ | ✅ | ❌ | MAVLink-based |
| **Advanced** |
| | `mavlink_mitm.py` | ❌ | ❌ | ✅ | ❌ | Network MITM |
| | `command_replay.py` | ❌ | ❌ | ✅ | ❌ | Network capture |
| | `telemetry_replay.py` | ❌ | ❌ | ✅ | ❌ | Network capture |
| | `arp_spoofing.py` | ⚠️ Optional | ❌ | ✅ | ❌ | Network MITM |
| | `dns_spoofing.py` | ⚠️ Optional | ❌ | ✅ | ❌ | Network MITM |
| **Firmware** |
| | `firmware_extraction.py` | ❌ | ❌ | ✅ | ❌ | Physical access |
| | `firmware_analysis.py` | ❌ | ❌ | ❌ | ❌ | Software-only |

**Legend**:
- ✅ **Required**: Hardware is essential for the exploit
- ⚠️ **Optional**: Hardware enhances the attack but not strictly required
- ❌ **Not Required**: Exploit works without this hardware

---

## Recommended Hardware Kits

### Starter Kit (Basic WiFi Attacks)
**Price**: ~$50-70
- Alfa AWUS036NHA WiFi adapter
- USB extension cable
- Kali Linux compatible system

**Use Cases**:
- WiFi cracking
- WiFi deauthentication
- Basic packet sniffing

### Intermediate Kit (WiFi + Network Attacks)
**Price**: ~$100-150
- Alfa AWUS036ACH WiFi adapter (dual-band)
- USB Ethernet adapter
- USB extension cable
- Kali Linux compatible system

**Use Cases**:
- All WiFi attacks
- Network MITM attacks
- ARP/DNS spoofing
- Packet capture

### Advanced Kit (Full Capabilities)
**Price**: ~$250-350
- Alfa AWUS036ACH WiFi adapter
- HackRF One SDR
- USB Ethernet adapter
- USB extension cables
- External antennas (optional)
- Kali Linux compatible system

**Use Cases**:
- All WiFi attacks
- RF/radio attacks (ExpressLRS)
- GPS spoofing (RF-based)
- Network attacks
- Complete exploit coverage

### Professional Kit (Research & Development)
**Price**: ~$500-800
- Alfa AWUS036ACH WiFi adapter
- HackRF One or BladeRF 2.0
- Multiple WiFi adapters (for multi-interface attacks)
- USB Ethernet adapters
- High-gain antennas
- Signal amplifiers (optional)
- Dedicated Kali Linux system

**Use Cases**:
- Advanced RF research
- Multi-vector attacks
- Signal analysis
- Protocol reverse engineering

---

## Hardware Setup Instructions

### WiFi Adapter Setup

1. **Install Drivers** (if needed):
```bash
# For Realtek RTL8812AU (Alfa AWUS036ACH)
sudo apt update
sudo apt install dkms
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install
```

2. **Verify Monitor Mode Support**:
```bash
# List WiFi interfaces
iwconfig

# Put interface in monitor mode
sudo airmon-ng start wlan0

# Verify monitor mode
iwconfig wlan0mon
```

3. **Test Packet Injection**:
```bash
# Test injection capability
sudo aireplay-ng -9 wlan0mon
```

### HackRF One Setup

1. **Install HackRF Tools**:
```bash
sudo apt update
sudo apt install hackrf libhackrf-dev hackrf-tools
```

2. **Verify HackRF Detection**:
```bash
hackrf_info
```

3. **Test Reception**:
```bash
# Receive on 433 MHz (ISM band)
hackrf_transfer -r capture.raw -f 433000000 -s 2000000
```

4. **Test Transmission** (use with caution):
```bash
# Transmit test signal
hackrf_transfer -t test.raw -f 433000000 -s 2000000
```

### Network Adapter Setup

1. **Enable Promiscuous Mode**:
```bash
# For Ethernet interface
sudo ifconfig eth0 promisc

# Verify
ifconfig eth0
```

2. **Test Packet Capture**:
```bash
# Capture packets
sudo tcpdump -i eth0 -w capture.pcap
```

---

## Simulator vs Real Hardware

### What Works in Simulator (No Hardware Needed)

✅ **All MAVLink-based exploits** work in the simulator:
- Command injection
- Parameter manipulation
- Mission extraction
- GPS spoofing (via MAVLink)
- Battery/attitude spoofing
- Communication flooding
- Flight termination

✅ **Network-based exploits** work with virtual networks:
- ARP spoofing (simulated)
- DNS spoofing (simulated)
- MITM attacks (simulated)
- Packet sniffing (simulated)

### What Requires Real Hardware

⚠️ **WiFi attacks** require real WiFi adapter:
- WiFi cracking (WEP/WPA2)
- WiFi deauthentication
- Real-world packet injection

⚠️ **RF attacks** require SDR hardware:
- ExpressLRS UID leakage
- RF GPS spoofing
- Radio frequency analysis

⚠️ **Physical access attacks**:
- Firmware extraction (requires physical access to flight controller)
- Hardware debugging interfaces (JTAG/SWD)

---

## Troubleshooting

### WiFi Adapter Not Detected

```bash
# Check USB devices
lsusb

# Check kernel modules
lsmod | grep -i rtl

# Reload drivers
sudo modprobe -r rtl8812au
sudo modprobe rtl8812au
```

### Monitor Mode Not Working

```bash
# Kill interfering processes
sudo airmon-ng check kill

# Try different method
sudo iw dev wlan0 set type monitor
sudo ifconfig wlan0 up
```

### HackRF Not Detected

```bash
# Check USB permissions
lsusb | grep HackRF

# Add user to plugdev group
sudo usermod -aG plugdev $USER
# Log out and back in

# Check udev rules
ls -la /etc/udev/rules.d/ | grep hackrf
```

---

## Legal Disclaimer

⚠️ **IMPORTANT**: This hardware is for **educational and authorized security testing only**. 

- Only use on systems you own or have explicit written permission to test
- Unauthorized access to computer systems is illegal
- Radio frequency transmission may require licenses in your jurisdiction
- Always comply with local laws and regulations
- The authors are not responsible for misuse of this information

---

## Additional Resources

- [Aircrack-ng Hardware Compatibility](https://www.aircrack-ng.org/doku.php?id=compatible_cards)
- [HackRF One Documentation](https://greatscottgadgets.com/hackrf/)
- [Kali Linux Hardware Compatibility](https://www.kali.org/docs/installation/hardware-requirements/)
- [WiFi Adapter Buying Guide](https://null-byte.wonderhowto.com/how-to/buy-best-wireless-adapter-for-wi-fi-hacking-2019-0178550/)

---

## Summary

**Minimum Setup** (Simulator Only):
- No additional hardware needed
- Works with built-in network adapters
- All MAVLink exploits functional

**Recommended Setup** (WiFi Attacks):
- Alfa AWUS036ACH WiFi adapter (~$50-70)
- Enables WiFi cracking and deauth attacks

**Complete Setup** (All Exploits):
- Alfa AWUS036ACH WiFi adapter
- HackRF One SDR (~$100-150)
- Enables RF attacks and ExpressLRS exploitation

For most educational purposes, the simulator works without additional hardware. Real hardware is only needed for:
1. Real-world WiFi attack testing
2. RF/radio frequency attacks
3. Physical hardware exploitation
