# How to Use This Repository

## 📖 Table of Contents

1. [Getting Started](#getting-started)
2. [Understanding the Repository Structure](#understanding-the-repository-structure)
3. [Setting Up the Simulator](#setting-up-the-simulator)
4. [Using the Web Interfaces](#using-the-web-interfaces)
5. [Running Attack Scenarios](#running-attack-scenarios)
6. [Using Exploit Scripts](#using-exploit-scripts)
7. [Configuration Management](#configuration-management)
8. [Progress Tracking](#progress-tracking)
9. [Exporting Data](#exporting-data)
10. [Troubleshooting](#troubleshooting)
11. [Best Practices](#best-practices)

---

## Getting Started

### Prerequisites

Before you begin, ensure you have:

- **Docker** installed and running
- **Docker Compose** installed
- **Kali Linux** (recommended) or compatible Linux distribution
- **Minimum System Requirements**:
  - **Lite Mode**: 4-8 GB RAM, 2 CPU cores, 100 GB disk
  - **Full Mode**: 8-16 GB RAM, 2-4 CPU cores, 100 GB disk, GPU with 2GB+ VRAM

### Quick Start Checklist

1. ✅ Docker is installed and running
2. ✅ Navigate to the simulator directory
3. ✅ Choose your mode (Lite or Full)
4. ✅ Start the simulator
5. ✅ Access the web interfaces
6. ✅ Begin exploring attack scenarios

---

## Understanding the Repository Structure

### Main Components

```
Drone Research/
├── Documentation Files (Top Level)
│   ├── README.md                    # Project overview
│   ├── USAGE_GUIDE.md               # This file
│   ├── SETUP_GUIDE.md               # Detailed setup instructions
│   ├── RESEARCH.md                   # Research documentation
│   └── ...
│
└── Damn-Vulnerable-Drone/            # Main simulator
    ├── companion-computer/          # Web UI (Port 3000)
    ├── simulator/                   # Management Console (Port 8000)
    ├── exploits/                    # Automated exploit scripts
    └── ...
```

### Key Directories

- **`Damn-Vulnerable-Drone/`** - Main simulator implementation
- **`Damn-Vulnerable-Drone/companion-computer/`** - Companion computer web interface
- **`Damn-Vulnerable-Drone/simulator/`** - Management console and attack scenarios
- **`Damn-Vulnerable-Drone/exploits/`** - Automated exploit scripts and chains

---

## Setting Up the Simulator

### Step 1: Navigate to Simulator Directory

```bash
cd "Drone Research/Drone /Damn-Vulnerable-Drone"
```

### Step 2: Choose Your Mode

#### Option A: Lite Mode (Recommended for First Time)
- No GPU required
- Faster setup
- 2D lightweight simulator
- Lower system requirements

```bash
# Pull pre-built images
docker compose -f docker-compose-lite.yaml pull

# OR build from source
docker compose -f docker-compose-lite.yaml build
```

#### Option B: Full Mode (3D Environment)
- Requires GPU with 2GB+ VRAM
- Gazebo 3D simulator
- More realistic experience

```bash
# Pull pre-built images
docker compose -f docker-compose.yaml pull

# OR build from source
docker compose -f docker-compose.yaml build
```

### Step 3: Start the Simulator

#### Lite Mode:
```bash
# Start without Wi-Fi (easier for first time)
sudo ./start.sh --mode lite --no-wifi

# OR start with Wi-Fi network (more realistic)
sudo ./start.sh --mode lite --wifi wpa2
```

#### Full Mode:
```bash
# Start without Wi-Fi
sudo ./start.sh --mode full --no-wifi

# OR start with Wi-Fi network
sudo ./start.sh --mode full --wifi wpa2
```

### Step 4: Verify Installation

Check that all containers are running:
```bash
sudo ./status.sh
```

You should see:
- ✅ flight-controller
- ✅ companion-computer
- ✅ ground-control-station
- ✅ simulator

---

## Hardware Requirements for Exploits

> 📖 **Detailed Hardware Guide**: See [HARDWARE_REQUIREMENTS.md](HARDWARE_REQUIREMENTS.md) for complete information about WiFi adapters, HackRF One, and other hardware.

### Quick Reference

- **WiFi Attacks** (wifi_crack.py, wifi_deauth.py): Requires WiFi adapter with monitor mode support
  - Recommended: Alfa AWUS036ACH (~$50-70)
  - Alternative: Alfa AWUS036NHA (~$30-40)

- **RF/Radio Attacks** (expresslrs_uid_leakage.py): Requires SDR device
  - Recommended: HackRF One (~$100-150)
  - Alternative: BladeRF 2.0 Micro (~$200-300)

- **Network Attacks** (arp_spoofing.py, dns_spoofing.py): Standard Ethernet adapter works fine

- **Most MAVLink Exploits**: No additional hardware needed (work in simulator)

---

## Using the Web Interfaces

### Management Console (Port 8000)

**URL**: http://localhost:8000

This is your main control center for:
- Viewing attack scenarios
- Triggering flight states
- Monitoring progress
- Exporting data

#### Main Features:

1. **Flight States** - Control drone flight states:
   - Initial Boot
   - Arm & Takeoff
   - Autopilot Flight
   - Emergency / Return-To-Land
   - Post-Flight Data Processing

2. **Attack Scenarios** - Browse 40+ attack scenarios organized by category:
   - Reconnaissance (7 scenarios)
   - Protocol Tampering (8 scenarios)
   - Denial of Service (7 scenarios)
   - Injection (10 scenarios)
   - Exfiltration (6 scenarios)
   - Firmware Attacks (2 scenarios)

3. **Dashboard** - View statistics and progress

4. **Learning Guides** - Access tutorials and walkthroughs

### Companion Computer Interface (Port 3000)

**URL**: http://localhost:3000

**Default Credentials**:
- Username: `admin`
- Password: `cyberdrone`

#### Main Features:

1. **Telemetry** - Real-time MAVLink telemetry data
2. **Wi-Fi Network** - Configure and manage Wi-Fi settings
3. **Camera Stream** - View RTSP camera feed
4. **Flight Logs** - Access and download flight logs
5. **Configuration** - Manage system configuration

---

## Running Attack Scenarios

### Method 1: Using the Web Interface

1. **Access Management Console**: http://localhost:8000
2. **Navigate to Attacks**: Click "Attacks" in the navigation menu
3. **Browse Categories**: Select a category (Reconnaissance, Injection, etc.)
4. **Select Scenario**: Click on an attack scenario
5. **View Details**: Read the scenario description and walkthrough
6. **Follow Instructions**: Execute the attack steps manually

### Method 2: Using Exploit Scripts

Navigate to the exploits directory:
```bash
cd "Drone Research/Drone /Damn-Vulnerable-Drone/exploits"
```

#### Available Exploit Scripts:

**Reconnaissance**:
```bash
# Wi-Fi Cracking
python3 recon/wifi_crack.py wlan0mon Drone_Wifi 6 02:00:00:00:01:00

# Drone Discovery
python3 recon/drone_discovery.py 192.168.13.0/24
```

**Injection**:
```bash
# MAVLink Command Injection
python3 injection/mavlink_inject.py udp:127.0.0.1:14550 SET_MODE

# Waypoint Override
python3 injection/waypoint_override.py udp:127.0.0.1:14550 47.3566 8.5461 10
```

**Denial of Service**:
```bash
# Wi-Fi Deauthentication
python3 dos/wifi_deauth.py wlan0mon 02:00:00:00:01:00 100
```

### Method 3: Using Attack Chains

Execute multi-stage attack chains:
```bash
cd exploits/chains

# List available chains
python3 chain_executor.py

# Execute a chain
python3 chain_executor.py full_takeover interface=wlan0mon ssid=Drone_Wifi
```

---

## Using Exploit Scripts

### Prerequisites

Ensure you have required tools installed:
```bash
# For Wi-Fi attacks
sudo apt-get install aircrack-ng

# For MAVLink
pip3 install pymavlink
```

### Script Categories

#### 1. Reconnaissance Scripts (`exploits/recon/`)

**wifi_crack.py** - Crack Wi-Fi encryption
```bash
python3 recon/wifi_crack.py <interface> <ssid> [channel] [bssid]
```

**drone_discovery.py** - Discover drones on network
```bash
python3 recon/drone_discovery.py <network_cidr>
```

#### 2. Injection Scripts (`exploits/injection/`)

**mavlink_inject.py** - Inject MAVLink commands
```bash
python3 injection/mavlink_inject.py <connection> <command> [params...]
```

Available commands:
- `SET_MODE` - Change flight mode
- `TAKEOFF` - Takeoff command
- `LAND` - Land command
- `RTL` - Return to launch
- `FLIGHT_TERMINATION` - Terminate flight

**waypoint_override.py** - Override waypoints
```bash
python3 injection/waypoint_override.py <connection> <lat> <lon> <alt>
```

#### 3. DoS Scripts (`exploits/dos/`)

**wifi_deauth.py** - Wi-Fi deauthentication attack
```bash
python3 dos/wifi_deauth.py <interface> <target_mac> [count]
```

### Using the Exploits API

You can also execute exploits via the REST API:

```bash
# List available exploits
curl http://localhost:8000/exploits/list

# Execute an exploit
curl -X POST http://localhost:8000/exploits/execute/wifi-analysis-cracking \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "script_path": "recon/wifi_crack.py", "args": ["wlan0mon", "Drone_Wifi"]}'

# Check execution status
curl http://localhost:8000/exploits/status/<execution_id>
```

---

## Configuration Management

### Accessing Configuration

**Via Web Interface**:
- Companion Computer: http://localhost:3000/config
- Management Console: Configuration options in settings

**Via API**:
```bash
# Get current configuration
curl http://localhost:3000/config

# Update configuration
curl -X POST http://localhost:3000/config \
  -H "Content-Type: application/json" \
  -d '{"security_level": "low", "wifi_encryption": "wep"}'
```

### Configuration Presets

Apply predefined configurations:

```bash
# List available presets
curl http://localhost:3000/config/presets

# Apply a preset
curl -X POST http://localhost:3000/config/preset/beginner
```

Available presets:
- **beginner** - Low security, all attacks enabled
- **intermediate** - Medium security, some mitigations
- **advanced** - High security, most mitigations
- **realistic** - Real-world configuration

### Configuration Options

Key configuration parameters:

- `security_level` - low, medium, high
- `wifi_encryption` - wep, wpa2, wpa3
- `mavlink_auth` - true/false
- `attack_difficulty` - beginner, intermediate, advanced
- `enable_geofence` - true/false
- `telemetry_rate` - Messages per second

---

## Progress Tracking

### Viewing Your Progress

**Via Web Interface**:
1. Navigate to http://localhost:8000
2. Click on "Dashboard" or "Progress"
3. View completion statistics

**Via API**:
```bash
# Get user progress
curl http://localhost:8000/progress/user/<user_id>

# Get scenario progress
curl http://localhost:8000/progress/scenario/<scenario_id>

# Get overall statistics
curl http://localhost:8000/progress/stats
```

### Updating Progress

```bash
# Update scenario progress
curl -X POST http://localhost:8000/progress/update \
  -H "Content-Type: application/json" \
  -d '{
    "scenario_id": "wifi-analysis-cracking",
    "user_id": "test_user",
    "status": "completed"
  }'
```

Status options:
- `not_started` - Not yet attempted
- `in_progress` - Currently working on
- `completed` - Successfully completed

---

## Exporting Data

### Export Attack Logs

**Via Web Interface**:
1. Navigate to http://localhost:8000
2. Go to "Export" section
3. Select format (JSON or CSV)
4. Download file

**Via API**:
```bash
# Export as JSON
curl http://localhost:8000/export/attack-logs?format=json -o attack_logs.json

# Export as CSV
curl http://localhost:8000/export/attack-logs?format=csv -o attack_logs.csv

# Export with filters
curl "http://localhost:8000/export/attack-logs?format=json&user_id=test_user&scenario_id=wifi-analysis-cracking" -o filtered_logs.json
```

### Export Completion Reports

```bash
# User-specific report
curl http://localhost:8000/export/completion-report?user_id=test_user&format=json

# Overall statistics
curl http://localhost:8000/export/completion-report?format=csv
```

### Export Exploit Executions

```bash
curl http://localhost:8000/export/exploit-executions?format=json -o executions.json
```

---

## Troubleshooting

### Common Issues

#### 1. Docker Permission Denied

**Problem**: Cannot run Docker commands without sudo

**Solution**:
```bash
sudo usermod -aG docker $USER
# Log out and back in for changes to take effect
```

#### 2. Port Already in Use

**Problem**: Port 8000 or 3000 already in use

**Solution**:
```bash
# Stop the simulator
sudo ./stop.sh

# Wait a few seconds, then start again
sudo ./start.sh --mode lite --no-wifi
```

#### 3. Containers Not Starting

**Problem**: Containers fail to start or crash

**Solution**:
```bash
# Check container logs
docker logs flight-controller
docker logs companion-computer
docker logs simulator

# Clean up and restart
sudo ./stop.sh
docker system prune -a
sudo ./start.sh --mode lite --no-wifi
```

#### 4. Out of Memory

**Problem**: System runs out of memory

**Solution**:
- Use Lite Mode instead of Full Mode
- Close other applications
- Increase swap space
- Reduce number of running containers

#### 5. Cannot Access Web Interfaces

**Problem**: Cannot connect to http://localhost:8000 or http://localhost:3000

**Solution**:
```bash
# Check if containers are running
sudo ./status.sh

# Check if ports are listening
netstat -tuln | grep -E '8000|3000'

# Check firewall settings
sudo ufw status
```

#### 6. Wi-Fi Mode Not Working

**Problem**: Wi-Fi network not appearing

**Solution**:
- Ensure you're running on Kali Linux or compatible system
- Check if hostapd is installed
- Verify network interface permissions
- Try non-Wi-Fi mode first: `--no-wifi`

### Getting Help

1. **Check Logs**: Review `dvd.log` in the project directory
2. **Container Logs**: Use `docker logs <container-name>`
3. **Status Script**: Run `sudo ./status.sh` for system status
4. **Documentation**: Review SETUP_GUIDE.md for detailed instructions

---

## Best Practices

### Learning Path

1. **Start with Lite Mode** - Easier setup, no GPU required
2. **Begin with Reconnaissance** - Learn basic information gathering
3. **Progress to Injection** - Understand command injection
4. **Explore DoS Attacks** - Learn denial of service techniques
5. **Study Exfiltration** - Understand data extraction
6. **Advanced Scenarios** - Tackle firmware attacks last

### Security Best Practices

1. **Use in Isolated Environment** - Never run on production systems
2. **Keep Documentation Updated** - Document your findings
3. **Follow Responsible Disclosure** - Report vulnerabilities properly
4. **Understand Legal Implications** - Only test systems you own or have permission
5. **Regular Updates** - Keep Docker images and dependencies updated

### Development Workflow

1. **Make Changes** - Edit source code in appropriate directories
2. **Rebuild Containers** - Use `docker compose build`
3. **Test Changes** - Restart simulator and verify functionality
4. **Update Documentation** - Keep CHANGELOG.md updated
5. **Commit Changes** - Use meaningful commit messages

### Performance Tips

1. **Use Lite Mode** - For faster startup and lower resource usage
2. **Close Unused Containers** - Stop containers you're not using
3. **Monitor Resources** - Use `docker stats` to monitor usage
4. **Clean Up Regularly** - Run `docker system prune` periodically

---

## Quick Reference

### Essential Commands

```bash
# Start simulator (Lite Mode, no Wi-Fi)
sudo ./start.sh --mode lite --no-wifi

# Start simulator (Full Mode, with Wi-Fi)
sudo ./start.sh --mode full --wifi wpa2

# Stop simulator
sudo ./stop.sh

# Check status
sudo ./status.sh

# View logs
tail -f dvd.log

# Access web interfaces
# Management: http://localhost:8000
# Companion: http://localhost:3000 (admin/cyberdrone)
```

### Key URLs

- **Management Console**: http://localhost:8000
- **Companion Computer**: http://localhost:3000
- **Default Credentials**: admin / cyberdrone

### Important Files

- `docker-compose.yaml` - Full mode configuration
- `docker-compose-lite.yaml` - Lite mode configuration
- `start.sh` - Startup script
- `stop.sh` - Cleanup script
- `status.sh` - Status check script
- `dvd.log` - Main log file

---

## Next Steps

1. **Read SETUP_GUIDE.md** - For detailed installation instructions
2. **Explore RESEARCH.md** - For comprehensive vulnerability research
3. **Review VULNERABILITIES_AND_EXPLOITS.md** - For detailed attack scenarios
4. **Check SUMMARY.md** - For quick reference
5. **Study Attack Scenarios** - Start with beginner scenarios
6. **Experiment with Exploits** - Try automated exploit scripts
7. **Track Your Progress** - Use the progress tracking features

---

## Additional Resources

- **Official Documentation**: See README.md for complete overview
- **Setup Instructions**: See SETUP_GUIDE.md for detailed setup
- **Research**: See RESEARCH.md for comprehensive research
- **Vulnerabilities**: See VULNERABILITIES_AND_EXPLOITS.md for attack details
- **Repository Catalog**: See REPOSITORIES.md for related projects

---

**Last Updated**: January 22, 2026  
**Repository Version**: 1.3.1

For questions or issues, refer to the troubleshooting section or review the comprehensive documentation files.
