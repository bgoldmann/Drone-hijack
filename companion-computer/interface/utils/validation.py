"""
Input validation utilities for flight controller interface
"""
import re
import os
from typing import Tuple, Optional
from pathlib import Path

# Standard baud rates for serial communication
STANDARD_BAUD_RATES = [9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600]

# IP address regex pattern
IP_PATTERN = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')

# Valid serial device path patterns
SERIAL_DEVICE_PATTERN = re.compile(r'^/dev/(tty|cu)[A-Za-z0-9]+$')


def validate_ip_address(ip: str) -> Tuple[bool, Optional[str]]:
    """
    Validate IP address format
    
    Args:
        ip: IP address string
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not ip or not isinstance(ip, str):
        return False, "IP address must be a non-empty string"
    
    if len(ip) > 15:  # Maximum IP address length
        return False, "IP address too long"
    
    if not IP_PATTERN.match(ip):
        return False, "Invalid IP address format"
    
    # Validate each octet is 0-255
    try:
        octets = ip.split('.')
        if len(octets) != 4:
            return False, "IP address must have 4 octets"
        
        for octet in octets:
            value = int(octet)
            if not 0 <= value <= 255:
                return False, f"IP octet {octet} out of range (0-255)"
    except ValueError:
        return False, "IP address contains non-numeric octets"
    
    return True, None


def validate_port(port: int) -> Tuple[bool, Optional[str]]:
    """
    Validate port number
    
    Args:
        port: Port number
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(port, int):
        return False, "Port must be an integer"
    
    if not 1 <= port <= 65535:
        return False, "Port must be between 1 and 65535"
    
    return True, None


def validate_udp_destination(ip: str, port: int) -> Tuple[bool, Optional[str]]:
    """
    Validate UDP destination IP and port
    
    Args:
        ip: IP address
        port: Port number
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    ip_valid, ip_error = validate_ip_address(ip)
    if not ip_valid:
        return False, ip_error
    
    port_valid, port_error = validate_port(port)
    if not port_valid:
        return False, port_error
    
    # Check for localhost restrictions (optional security check)
    if ip in ['127.0.0.1', 'localhost', '::1']:
        # Allow localhost but log it
        pass
    
    return True, None


def validate_serial_device(device: str) -> Tuple[bool, Optional[str]]:
    """
    Validate serial device path
    
    Args:
        device: Serial device path
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not device or not isinstance(device, str):
        return False, "Serial device must be a non-empty string"
    
    if len(device) > 100:  # Reasonable path length limit
        return False, "Serial device path too long"
    
    # Check for path traversal attempts
    if '..' in device or device.startswith('/') and '//' in device:
        return False, "Invalid serial device path (path traversal detected)"
    
    # Validate format (Linux/Unix serial devices)
    if not SERIAL_DEVICE_PATTERN.match(device):
        # Allow other valid paths but be cautious
        if not device.startswith('/dev/'):
            return False, "Serial device must be in /dev/ directory"
    
    # Additional security: check for dangerous paths
    dangerous_patterns = ['/proc', '/sys', '/etc', '/root', '/home']
    for pattern in dangerous_patterns:
        if pattern in device:
            return False, f"Serial device path contains dangerous pattern: {pattern}"
    
    return True, None


def validate_baud_rate(baud: int) -> Tuple[bool, Optional[str]]:
    """
    Validate baud rate
    
    Args:
        baud: Baud rate value
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(baud, int):
        return False, "Baud rate must be an integer"
    
    if baud not in STANDARD_BAUD_RATES:
        # Allow non-standard but warn
        if baud < 300 or baud > 2000000:
            return False, f"Baud rate {baud} out of reasonable range (300-2000000)"
        # Non-standard but within range - allow with warning
        return True, f"Warning: Baud rate {baud} is not a standard value"
    
    return True, None


def validate_parameter_name(name: str) -> Tuple[bool, Optional[str]]:
    """
    Validate and sanitize parameter name
    
    Args:
        name: Parameter name
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name or not isinstance(name, str):
        return False, "Parameter name must be a non-empty string"
    
    if len(name) > 16:  # ArduPilot parameter names are max 16 chars
        return False, "Parameter name exceeds maximum length (16 characters)"
    
    # Check for injection attempts
    dangerous_chars = [';', '&', '|', '`', '$', '(', ')', '<', '>', '\n', '\r']
    for char in dangerous_chars:
        if char in name:
            return False, f"Parameter name contains invalid character: {char}"
    
    # ArduPilot parameter names are alphanumeric with underscores
    if not re.match(r'^[A-Z0-9_]+$', name):
        return False, "Parameter name must contain only uppercase letters, numbers, and underscores"
    
    return True, None


def validate_parameter_value(value: any, param_type: str = 'REAL32') -> Tuple[bool, Optional[str]]:
    """
    Validate parameter value based on type
    
    Args:
        value: Parameter value
        param_type: Parameter type (REAL32, INT32, etc.)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if value is None:
        return False, "Parameter value cannot be None"
    
    # Convert to appropriate type
    try:
        if param_type in ['REAL32', 'REAL64']:
            float_value = float(value)
            # Check for NaN or Infinity
            if not (float('-inf') < float_value < float('inf')):
                return False, "Parameter value is NaN or Infinity"
        elif param_type in ['INT32', 'INT16', 'INT8', 'UINT32', 'UINT16', 'UINT8']:
            int_value = int(value)
            # Check ranges based on type
            if 'UINT' in param_type:
                if int_value < 0:
                    return False, f"Parameter value must be non-negative for {param_type}"
        else:
            # Default: try to convert to float
            float(value)
    except (ValueError, TypeError) as e:
        return False, f"Invalid parameter value type: {e}"
    
    return True, None
