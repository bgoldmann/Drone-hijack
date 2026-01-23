# Flight Controller Review

**Date**: January 22, 2026  
**Component**: Flight Controller (ArduPilot-based)  
**Status**: Review Complete

---

## Executive Summary

The flight controller is based on **ArduPilot Copter 4.6.3** running in a Docker container. It uses ArduPilot's SITL (Software-In-The-Loop) simulator and communicates via MAVLink protocol. The implementation includes a web-based management interface through the companion computer.

### Key Components

1. **Docker Container** (`flight-controller/Dockerfile`)
   - ArduPilot Copter 4.6.3
   - MAVLink communication
   - Serial communication via socat

2. **Initialization Script** (`flight-controller/init.sh`)
   - Sets up serial communication bridge
   - Creates Unix socket for inter-container communication

3. **Parameter File** (`flight-controller/drone.parm`)
   - 1373+ ArduPilot parameters
   - Flight control, sensor, and safety configurations

4. **Web Interface** (`companion-computer/interface/`)
   - Flight controller management UI
   - Telemetry monitoring
   - MAVLink connection management

---

## Architecture Overview

### Container Setup

```
flight-controller (10.13.0.2)
├── ArduPilot SITL
├── MAVLink Protocol (UDP:5760, TCP:9003)
├── Serial Bridge (socat → /dev/ttyACM0)
└── Unix Socket (/sockets/socket.sock)
```

### Communication Flow

```
Flight Controller → MAVLink → Companion Computer → Web UI
                  ↓
              Simulator (Gazebo)
```

### Network Configuration

- **IP Address**: 10.13.0.2
- **Exposed Ports**: 5760 (MAVLink), 9003 (TCP)
- **Network**: `simulator` bridge network
- **Privileged**: Yes (required for serial access)

---

## Security Issues Identified

### 🔴 Critical Issues

#### 1. **Privileged Container**
```yaml
privileged: true
```
**Issue**: Container runs with full host privileges  
**Risk**: Complete system compromise if container is breached  
**Impact**: HIGH  
**Recommendation**: Use specific capabilities instead of privileged mode

#### 2. **No MAVLink Authentication**
**Issue**: MAVLink 1.0/2.0 used without package signing  
**Risk**: Message injection, replay attacks, MITM  
**Impact**: CRITICAL  
**Evidence**: 
- No authentication in `mavlink_connection.py`
- No signature verification
- Default MAVLink protocol (no encryption)

**Recommendation**: 
- Enable MAVLink 2.0 package signing
- Implement HMAC-based authentication
- Use MAVSec extensions for encryption

#### 3. **Unrestricted Parameter Access**
**Issue**: Parameters can be read/modified without authentication  
**Risk**: Safety feature bypass, flight control manipulation  
**Impact**: HIGH  
**Evidence**: `set_parameter()` function in `mavlink_connection.py` has no access control

**Recommendation**:
- Implement parameter access control
- Whitelist safe parameters for modification
- Require authentication for critical parameters

#### 4. **Insecure Serial Communication**
**Issue**: Serial port permissions set to `a+rw` (world-writable)  
**Risk**: Unauthorized access to flight controller  
**Impact**: MEDIUM  
**Evidence**: `init.sh` line 13: `sudo chmod a+rw /dev/ttyACM0`

**Recommendation**:
- Use proper group permissions
- Implement access control

### 🟡 Medium Issues

#### 5. **No Input Validation in Web Interface**
**Issue**: Web UI doesn't validate user inputs  
**Risk**: Command injection, parameter manipulation  
**Impact**: MEDIUM  
**Evidence**: `telemetry.py` accepts user inputs without validation

**Recommendation**:
- Validate all inputs (IP addresses, ports, baud rates)
- Sanitize parameter names and values
- Implement rate limiting

#### 6. **Process Management Vulnerabilities**
**Issue**: `mavlink-routerd` process management uses `kill -9`  
**Risk**: Race conditions, process hijacking  
**Impact**: MEDIUM  
**Evidence**: `telemetry.py` lines 99-105

**Recommendation**:
- Use proper process management (systemd, supervisor)
- Implement graceful shutdown
- Track process PIDs securely

#### 7. **No Error Handling for MAVLink Connection**
**Issue**: Missing timeout and error handling  
**Risk**: Hanging connections, resource exhaustion  
**Impact**: MEDIUM  
**Evidence**: `mavlink_connection.py` line 18: `wait_heartbeat()` without timeout

**Recommendation**:
- Add connection timeouts
- Implement retry logic
- Handle connection failures gracefully

### 🟢 Low Issues

#### 8. **Hardcoded Configuration Values**
**Issue**: Many hardcoded values in parameter file  
**Risk**: Difficult to maintain, potential misconfigurations  
**Impact**: LOW

#### 9. **No Logging of Critical Operations**
**Issue**: Limited logging of flight control operations  
**Risk**: Difficult to audit and debug  
**Impact**: LOW

---

## Code Quality Issues

### 1. **Error Handling**

**Issue**: Broad exception catching
```python
except Exception as e:
    print(f"[-] Error: {e}")
```

**Location**: Multiple files  
**Recommendation**: Use specific exception types

### 2. **Missing Input Validation**

**Issue**: No validation of:
- UDP destination IPs/ports
- Baud rates
- Serial device paths
- Parameter values

**Recommendation**: Add comprehensive validation

### 3. **Resource Management**

**Issue**: No cleanup of:
- MAVLink connections
- Subprocess handles
- Socket connections

**Recommendation**: Implement proper cleanup

### 4. **Thread Safety**

**Issue**: Global variables without locks
```python
mav_connection = None  # Global, no locking
```

**Recommendation**: Use thread-safe patterns

---

## Configuration Review

### Parameter File Analysis

**Total Parameters**: 1373  
**Critical Parameters**:

1. **Safety Parameters**:
   - `BRD_SAFETYOPTION`: 3 (Enabled)
   - `FS_THR_ENABLE`: 1 (Enabled)
   - `FS_EKF_ACTION`: 1 (Enabled)
   - `FENCE_ENABLE`: 0 (Disabled) ⚠️

2. **Communication Parameters**:
   - `SERIAL0_PROTOCOL`: 2 (MAVLink)
   - `SERIAL1_PROTOCOL`: 2 (MAVLink)
   - `SERIAL2_PROTOCOL`: 2 (MAVLink)

3. **Flight Control Parameters**:
   - `FLTMODE1`: 7 (RTL)
   - `FLTMODE2`: 9 (LAND)
   - `FLTMODE3`: 6 (RTL)

### Security Configuration Issues

1. **Geofence Disabled**: `FENCE_ENABLE: 0`
   - **Risk**: No flight boundary restrictions
   - **Recommendation**: Enable geofence for production

2. **No MAVLink Signing**: Default configuration
   - **Risk**: Unauthenticated commands
   - **Recommendation**: Enable MAVLink 2.0 signing

3. **GPS Auto-Config**: `GPS_AUTO_CONFIG: 1`
   - **Risk**: Potential GPS spoofing
   - **Recommendation**: Validate GPS sources

---

## Recommendations

### Immediate Actions (High Priority)

1. **Enable MAVLink Authentication**
   ```python
   # Add to mavlink_connection.py
   connection = mavutil.mavlink_connection(
       'udp:0.0.0.0:14540',
       source_system=255,
       source_component=190,
       sign=True,  # Enable signing
       key=b'your-secret-key'
   )
   ```

2. **Add Input Validation**
   ```python
   def validate_udp_destination(ip, port):
       # Validate IP format
       # Validate port range (1-65535)
       # Check for localhost restrictions
   ```

3. **Implement Parameter Access Control**
   ```python
   CRITICAL_PARAMS = ['ARMING_CHECK', 'FS_THR_ENABLE', 'FENCE_ENABLE']
   def set_parameter(param_id, param_value):
       if param_id in CRITICAL_PARAMS:
           # Require authentication
           # Log access
   ```

4. **Fix Container Privileges**
   ```yaml
   # Instead of privileged: true
   cap_add:
     - SYS_ADMIN
     - NET_ADMIN
   devices:
     - /dev/ttyACM0:/dev/ttyACM0
   ```

### Medium Priority

5. **Add Comprehensive Logging**
   - Log all parameter changes
   - Log connection attempts
   - Log command executions

6. **Implement Rate Limiting**
   - Limit parameter change frequency
   - Limit connection attempts
   - Limit command execution rate

7. **Add Connection Timeouts**
   ```python
   connection.wait_heartbeat(timeout=5)  # Add timeout
   ```

### Low Priority

8. **Improve Error Messages**
   - More descriptive error messages
   - Actionable error guidance
   - User-friendly notifications

9. **Add Health Checks**
   - Monitor MAVLink connection health
   - Monitor process status
   - Alert on failures

10. **Documentation**
    - Document all parameters
    - Document security considerations
    - Document deployment procedures

---

## Testing Recommendations

### Security Testing

1. **MAVLink Injection Tests**
   - Test command injection
   - Test parameter manipulation
   - Test replay attacks

2. **Authentication Tests**
   - Test without authentication
   - Test with invalid credentials
   - Test session management

3. **Input Validation Tests**
   - Test invalid IP addresses
   - Test invalid ports
   - Test buffer overflows

### Functional Testing

1. **Connection Tests**
   - Test connection establishment
   - Test connection recovery
   - Test multiple connections

2. **Parameter Tests**
   - Test parameter reading
   - Test parameter writing
   - Test parameter validation

---

## Compliance & Standards

### OWASP Top 10 Drone Security Risks

**Current Status**:
- ❌ Insecure Communication (MAVLink unencrypted)
- ❌ Weak Authentication (No authentication)
- ⚠️ Insecure Firmware (ArduPilot 4.6.3 - check for CVEs)
- ❌ Inadequate Data Protection (No encryption)
- ❌ Insufficient Network Security (No network isolation)

### MAVLink Security Best Practices

**Current Status**:
- ❌ MAVLink 2.0 package signing: Not enabled
- ❌ Message authentication: Not implemented
- ❌ Encryption: Not implemented
- ⚠️ System ID enforcement: Partially implemented

---

## Conclusion

The flight controller implementation is **functional but insecure by design** (as intended for a vulnerable drone platform). For production use, significant security improvements are required:

1. **Critical**: Enable MAVLink authentication and encryption
2. **Critical**: Implement parameter access control
3. **High**: Fix container security (remove privileged mode)
4. **High**: Add comprehensive input validation
5. **Medium**: Implement proper error handling and logging

The current implementation serves its educational purpose well but should not be used in production environments without the recommended security enhancements.

---

## References

- ArduPilot Documentation: https://ardupilot.org/
- MAVLink Protocol: https://mavlink.io/
- OWASP Drone Security: https://owasp.org/
- CVE Database: https://cve.mitre.org/
