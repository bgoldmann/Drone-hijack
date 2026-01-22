# Damn Vulnerable Drone - Setup & Upgrade Guide

## ✅ Repository Successfully Downloaded!

The **Damn Vulnerable Drone** repository is located at:
```
Drone Research/Drone /Damn-Vulnerable-Drone/
```

---

## 📋 Quick Start

### Prerequisites Check

Before starting, ensure you have:

1. **Docker** installed and running
2. **Docker Compose** installed
3. **Kali Linux** (recommended) or compatible Linux distribution
4. **Minimum System Requirements**:
   - **Lite Mode**: 4-8 GB RAM, 2 CPU cores, 100 GB disk
   - **Full Mode**: 8-16 GB RAM, 2-4 CPU cores, 100 GB disk, GPU with 2GB+ VRAM

> 📖 **Hardware for Exploits**: While the simulator runs without additional hardware, some exploits require specific devices:
> - **WiFi Attacks**: Alfa AWUS036ACH or compatible WiFi adapter (see [HARDWARE_REQUIREMENTS.md](HARDWARE_REQUIREMENTS.md))
> - **RF Attacks**: HackRF One SDR for ExpressLRS and radio frequency attacks
> - **Network Attacks**: Standard Ethernet adapter works fine

---

## 🚀 Installation Steps

### Step 1: Install Docker (if not already installed)

On Kali Linux:

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

### Step 2: Navigate to Repository

```bash
cd "Drone Research/Drone /Damn-Vulnerable-Drone"
```

### Step 3: Choose Your Mode

#### Option A: Lite Mode (Recommended for First Time)
- No GPU required
- Faster setup
- 2D lightweight simulator
- Lower system requirements

```bash
# Pull pre-built images (faster)
docker compose -f docker-compose-lite.yaml pull

# OR build from source (slower but more control)
docker compose -f docker-compose-lite.yaml build
```

#### Option B: Full Mode (3D Environment)
- Requires GPU with 2GB+ VRAM
- Gazebo 3D simulator
- More realistic experience
- Higher system requirements

```bash
# Pull pre-built images
docker compose -f docker-compose.yaml pull

# OR build from source
docker compose -f docker-compose.yaml build
```

### Step 4: Start the Simulator

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

### Step 5: Access the Management Console

Once started, access the web interface at:
- **Management Console**: http://localhost:8000
- **QGroundControl**: Launched automatically (Full Mode only, x86 architecture)

---

## 🔧 Upgrade & Customization Guide

### Understanding the Repository Structure

```
Damn-Vulnerable-Drone/
├── companion-computer/     # Companion computer Docker container
│   ├── interface/         # Web UI (Flask/Python)
│   ├── conf/             # Configuration files
│   └── Dockerfile         # Container definition
├── flight-controller/    # ArduPilot flight controller
│   ├── drone.parm        # ArduPilot parameters
│   └── Dockerfile
├── ground-control-station/ # QGroundControl integration
│   ├── missions/         # Mission waypoints
│   └── stages/           # Flight stage scripts
├── simulator/            # Gazebo simulator files
│   └── mgmt/            # Management web console
├── docker-compose.yaml   # Full mode configuration
├── docker-compose-lite.yaml # Lite mode configuration
├── start.sh              # Start script
├── stop.sh               # Stop script
└── status.sh             # Status check script
```

### Areas for Upgrade & Improvement

#### 1. **Web Interface Enhancements** (`companion-computer/interface/`)
- **Location**: `companion-computer/interface/app.py`
- **Potential Upgrades**:
  - Add new attack scenario buttons
  - Improve UI/UX with modern frameworks
  - Add real-time telemetry visualization
  - Implement authentication improvements
  - Add logging and analytics

#### 2. **Attack Scenarios** (`simulator/mgmt/`)
- **Location**: `simulator/mgmt/`
- **Potential Upgrades**:
  - Add new vulnerability scenarios
  - Create advanced attack chains
  - Implement multi-stage exploits
  - Add automated exploit scripts

#### 3. **Flight Controller Parameters** (`flight-controller/drone.parm`)
- **Location**: `flight-controller/drone.parm`
- **Potential Upgrades**:
  - Add new vulnerable configurations
  - Create different drone models
  - Implement custom flight behaviors
  - Add sensor spoofing capabilities

#### 4. **Docker Configuration**
- **Files**: `docker-compose.yaml`, `docker-compose-lite.yaml`
- **Potential Upgrades**:
  - Optimize container sizes
  - Add health checks
  - Implement auto-restart policies
  - Add monitoring and logging

#### 5. **Documentation**
- **Location**: `README.md`, Wiki
- **Potential Upgrades**:
  - Add video tutorials
  - Create step-by-step guides
  - Document new features
  - Add troubleshooting section

---

## 🎯 Recommended Upgrade Path

### Phase 1: Understanding (Week 1-2)
1. Run the simulator in Lite Mode
2. Complete all basic attack scenarios
3. Review the codebase structure
4. Read through documentation

### Phase 2: Exploration (Week 3-4)
1. Examine source code in detail
2. Understand Docker architecture
3. Test different flight states
4. Experiment with attack scenarios

### Phase 3: Enhancement (Week 5+)
1. **Add New Attack Scenario**:
   - Create new vulnerability in flight controller
   - Add UI button for new scenario
   - Write documentation and walkthrough

2. **Improve Web Interface**:
   - Modernize UI with React/Vue
   - Add real-time charts
   - Improve user experience

3. **Extend Functionality**:
   - Add new drone models
   - Implement additional protocols
   - Create training modules

4. **Performance Optimization**:
   - Optimize Docker images
   - Reduce resource usage
   - Improve startup time

---

## 🔍 Key Files to Study for Upgrading

### Python Web Interface
- `companion-computer/interface/app.py` - Main Flask application
- `companion-computer/interface/routes/` - Route handlers
- `companion-computer/interface/models.py` - Data models

### Flight Controller
- `flight-controller/drone.parm` - ArduPilot parameters
- `flight-controller/init.sh` - Initialization script

### Simulator Management
- `simulator/mgmt/` - Management console code
- `start.sh` - Startup script (understand how it works)

### Docker Configuration
- `docker-compose.yaml` - Full mode setup
- `docker-compose-lite.yaml` - Lite mode setup
- Individual `Dockerfile` files in each component

---

## 🛠️ Development Workflow

### Making Changes

1. **Edit Source Code**:
   ```bash
   # Make your changes to Python files, configs, etc.
   nano companion-computer/interface/app.py
   ```

2. **Rebuild Containers**:
   ```bash
   # Stop current instance
   sudo ./stop.sh
   
   # Rebuild with your changes
   docker compose -f docker-compose-lite.yaml build
   
   # Start again
   sudo ./start.sh --mode lite --no-wifi
   ```

3. **Test Your Changes**:
   - Access http://localhost:8000
   - Test the functionality you modified
   - Check logs: `tail -f dvd.log`

### Contributing Back

1. **Fork the Repository** on GitHub
2. **Create a Branch** for your feature
3. **Make Your Changes**
4. **Test Thoroughly**
5. **Submit Pull Request** with:
   - Description of changes
   - Why the change is useful
   - Testing performed

---

## 📚 Learning Resources

### Official Documentation
- **Main README**: `Damn-Vulnerable-Drone/Readme.md`
- **Wiki**: https://github.com/nicholasaleks/Damn-Vulnerable-Drone/wiki
- **Attack Scenarios**: https://github.com/nicholasaleks/Damn-Vulnerable-Drone/wiki/Attack-Scenarios

### Related Technologies
- **ArduPilot**: https://ardupilot.org/
- **MAVLink**: https://mavlink.io/
- **Gazebo**: http://gazebosim.org/
- **Docker**: https://docs.docker.com/

### Community
- **Slack Channel**: https://join.slack.com/t/damnvulnerabledrone/shared_invite/zt-2g9tp202t-x5csb~uTyvHurgptki_XwQ
- **GitHub Issues**: https://github.com/nicholasaleks/Damn-Vulnerable-Drone/issues
- **Pull Requests**: https://github.com/nicholasaleks/Damn-Vulnerable-Drone/pulls

---

## 🐛 Troubleshooting

### Common Issues

1. **Docker Permission Denied**:
   ```bash
   sudo usermod -aG docker $USER
   # Log out and back in
   ```

2. **Port Already in Use**:
   ```bash
   sudo ./stop.sh
   # Wait a few seconds, then start again
   ```

3. **Out of Memory**:
   - Use Lite Mode instead of Full Mode
   - Close other applications
   - Increase swap space

4. **Container Build Fails**:
   ```bash
   # Clean Docker cache
   docker system prune -a
   # Try pulling pre-built images instead
   docker compose -f docker-compose-lite.yaml pull
   ```

---

## 📊 Current Status

- ✅ Repository cloned successfully
- ✅ Ready for setup and customization
- ✅ 233 commits (actively maintained)
- ✅ Comprehensive documentation available
- ✅ Multiple attack scenarios included

---

## 🎓 Next Steps

1. **Install Docker** (if not already installed)
2. **Start with Lite Mode** for easier setup
3. **Complete basic attack scenarios** to understand the system
4. **Review the codebase** to identify upgrade opportunities
5. **Start making improvements** based on your interests

---

**Good luck with your drone security research and upgrades!** 🚁🔒

---

---

**Last Updated**: January 22, 2026  
**Repository Version**: 1.3.1

For related documentation, see:
- **README.md** - Project overview and structure
- **RECOMMENDATION.md** - Repository selection guide
- **CHANGELOG.md** - Version history
