from flask import Blueprint, jsonify, request
import socketio
from extensions import db
from models import TelemetryStatus, UdpDestination
import subprocess
from pymavlink import mavutil
import logging
import threading
import serial.tools.list_ports
from flask import render_template
from mavlink_connection import close_mavlink_connection, set_parameter
from flask_login import login_required, current_user
import time
import signal
import os
from utils.validation import (
    validate_udp_destination, validate_serial_device, 
    validate_baud_rate, validate_parameter_name, validate_parameter_value
)
from utils.rate_limiter import rate_limit

telemetry_bp = Blueprint('telemetry', __name__)

# Add flight-controller template html render endpoint
@telemetry_bp.route('/flight-controller')
@login_required
def flight_controller():
    return render_template('flightController.html')

# Configure logging
logging.basicConfig(filename='/var/log/mavlink-routerd.log', level=logging.DEBUG)

# Security event logger
def log_security_event(event_type, details, user=None):
    """Log security events with structured format"""
    user_id = user.id if user and hasattr(user, 'id') else None
    username = user.username if user and hasattr(user, 'username') else 'anonymous'
    logging.info({
        'event': event_type,
        'timestamp': time.time(),
        'user_id': user_id,
        'username': username,
        'details': details
    })


def get_mavlink_routerd_pids():
    """Get all mavlink-routerd process PIDs"""
    try:
        result = subprocess.run(
            ["pgrep", "-f", "mavlink-routerd"],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            pids = [int(pid) for pid in result.stdout.strip().split('\n') if pid]
            return pids
        return []
    except (subprocess.CalledProcessError, ValueError, OSError) as e:
        logging.error(f"Error getting mavlink-routerd PIDs: {e}")
        return []


def stop_mavlink_routerd_gracefully(pid, timeout=5):
    """Stop mavlink-routerd process gracefully"""
    try:
        # Try SIGTERM first
        os.kill(pid, signal.SIGTERM)
        logging.info(f"Sent SIGTERM to mavlink-routerd PID {pid}")
        
        # Wait for process to terminate
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                os.kill(pid, 0)  # Check if process exists
                time.sleep(0.1)
            except ProcessLookupError:
                # Process terminated
                logging.info(f"mavlink-routerd PID {pid} terminated gracefully")
                return True
        
        # If still running, use SIGKILL
        logging.warning(f"mavlink-routerd PID {pid} did not terminate, using SIGKILL")
        os.kill(pid, signal.SIGKILL)
        return True
    except ProcessLookupError:
        # Process already terminated
        return True
    except (OSError, PermissionError) as e:
        logging.error(f"Error stopping mavlink-routerd PID {pid}: {e}")
        return False

@telemetry_bp.route('/start-telemetry', methods=['POST'])
@login_required
@rate_limit()
def start_telemetry():
    data = request.json
    
    # Validate input
    serial_device = data.get('serial_device')
    if not serial_device:
        return jsonify({'error': 'serial_device is required'}), 400
    
    device_valid, device_error = validate_serial_device(serial_device)
    if not device_valid:
        log_security_event('validation_failed', {'field': 'serial_device', 'error': device_error}, current_user)
        return jsonify({'error': f'Invalid serial device: {device_error}'}), 400
    
    baud_rate = data.get('baud_rate')
    if baud_rate is None:
        return jsonify({'error': 'baud_rate is required'}), 400
    
    baud_valid, baud_error = validate_baud_rate(baud_rate)
    if not baud_valid:
        log_security_event('validation_failed', {'field': 'baud_rate', 'error': baud_error}, current_user)
        return jsonify({'error': f'Invalid baud rate: {baud_error}'}), 400
    
    enable_udp_server = data.get('enable_udp_server', False)
    udp_server_port = data.get('udp_server_port', 14550)
    
    # Validate UDP server port
    port_valid, port_error = validate_port(udp_server_port)
    if not port_valid:
        log_security_event('validation_failed', {'field': 'udp_server_port', 'error': port_error}, current_user)
        return jsonify({'error': f'Invalid UDP server port: {port_error}'}), 400
    
    enable_tcp_server = data.get('enable_tcp_server', False)
    tcp_server_port = 5760 if enable_tcp_server else 0
    enable_datastream_requests = data.get('enable_datastream_requests', False)
    enable_heartbeat = data.get('enable_heartbeat', False)
    enable_tlogs = data.get('enable_tlogs', False)

    log_security_event('telemetry_start_attempt', {
        'serial_device': serial_device,
        'baud_rate': baud_rate,
        'udp_server_port': udp_server_port
    }, current_user)

    try:
        # Build the mavlink-routerd command
        cmd = [
            'mavlink-routerd',
            '-r',
            '-l', '/var/log/mavlink-router',
            '--tcp-port', str(tcp_server_port),
            serial_device + ':' + str(baud_rate)
        ]

        if enable_tlogs:
            cmd.extend(['-T'])

        if enable_udp_server:
            cmd.extend(['-p', f'0.0.0.0:{udp_server_port}'])

        udp_destinations = UdpDestination.query.all()
        for destination in udp_destinations:
            cmd.extend(['-e', f"{destination.ip}:{destination.port}"])

        # Start the process and make sure it's handled properly
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            logging.error(f"mavlink-routerd failed: {stderr.decode().strip()}")
            raise RuntimeError(f"mavlink-routerd failed: {stderr.decode().strip()}")

        # Update the telemetry status in the database
        telemetry_status_record = TelemetryStatus.query.first()
        if telemetry_status_record:
            telemetry_status_record.status = "Connecting"
        else:
            telemetry_status_record = TelemetryStatus(status="Connecting")
        db.session.add(telemetry_status_record)
        db.session.commit()

        log_security_event('telemetry_started', {
            'serial_device': serial_device,
            'baud_rate': baud_rate,
            'udp_server_port': udp_server_port,
            'process_id': process.pid if process else None
        }, current_user)

        return jsonify({'status': 'Telemetry started', 'cmd': ' '.join(cmd)})
    except (subprocess.CalledProcessError, OSError, PermissionError) as e:
        logging.error(f"Failed to start telemetry: {str(e)}")
        log_security_event('telemetry_start_failed', {
            'error': str(e),
            'error_type': type(e).__name__
        }, current_user)
        return jsonify({'error': f'Failed to start telemetry: {str(e)}'}), 500
    except (ValueError, TypeError) as e:
        logging.error(f"Invalid input for telemetry start: {str(e)}")
        log_security_event('telemetry_start_failed', {
            'error': str(e),
            'error_type': 'ValidationError'
        }, current_user)
        return jsonify({'error': f'Invalid input: {str(e)}'}), 400
    except Exception as e:
        logging.error(f"Unexpected error starting telemetry: {str(e)}")
        log_security_event('telemetry_start_failed', {
            'error': str(e),
            'error_type': type(e).__name__
        }, current_user)
        return jsonify({'error': 'An unexpected error occurred'}), 500

@telemetry_bp.route('/stop-telemetry', methods=['POST'])
@login_required
def stop_telemetry():
    log_security_event('telemetry_stop_attempt', {}, current_user)

    try:
        # Get all mavlink-routerd PIDs using improved method
        mavlink_routerd_pids = get_mavlink_routerd_pids()
        
        if not mavlink_routerd_pids:
            logging.info("No mavlink-routerd processes found")
            log_security_event('telemetry_stop', {'status': 'no_processes'}, current_user)
        else:
            # Stop each process gracefully
            for pid in mavlink_routerd_pids:
                stop_mavlink_routerd_gracefully(pid, timeout=5)
            
            log_security_event('telemetry_stop', {
                'status': 'stopped',
                'pids': mavlink_routerd_pids
            }, current_user)
    except (OSError, PermissionError) as e:
        logging.error(f"Error stopping telemetry: {e}")
        log_security_event('telemetry_stop_failed', {
            'error': str(e),
            'error_type': type(e).__name__
        }, current_user)
        return jsonify({'error': f'Failed to stop telemetry: {str(e)}'}), 500
    except Exception as e:
        logging.error(f"Unexpected error stopping telemetry: {e}")
        log_security_event('telemetry_stop_failed', {
            'error': str(e),
            'error_type': type(e).__name__
        }, current_user)

    try:
        # If a telemetry status record already exists, update it. Otherwise, create a new record.
        telemetry_status_record = TelemetryStatus.query.first()
        if telemetry_status_record:
            telemetry_status_record.status = "Not Connected"
        else:
            telemetry_status_record = TelemetryStatus(status="Not Connected")

        db.session.add(telemetry_status_record)
        db.session.commit()

        return jsonify({'status': 'Telemetry stopped'})
    except (subprocess.CalledProcessError, OSError, PermissionError) as e:
        logging.error(f"Error updating telemetry status: {e}")
        return jsonify({'error': f'Failed to update telemetry status: {str(e)}'}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@telemetry_bp.route('/telemetry-status', methods=['GET'])
def get_telemetry_status():
    telemetry_status = TelemetryStatus.query.first()

    # Double check status by checking for mavlink-routerd process, if process is running keep status as connected else update status to not connected
    if telemetry_status and telemetry_status.status == "Connected":
        try:
            subprocess.run(["pgrep", "-f", "mavlink-routerd"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            telemetry_status.status = "Not Connected"
            db.session.commit()
    # else if find "Connecting" status in db, check for mavlink-routerd process, if process is not running update status to not connected
    elif telemetry_status and telemetry_status.status == "Connecting":
        try:
            subprocess.run(["pgrep", "-f", "mavlink-routerd"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            telemetry_status.status = "Not Connected"
            db.session.commit()
    else:
        telemetry_status = TelemetryStatus(status="Not Connected")
        db.session.add(telemetry_status)
        db.session.commit()

    return jsonify({'isTelemetryRunning': telemetry_status.status})


@telemetry_bp.route('/serial-devices', methods=['GET'])
@login_required
def get_serial_devices():
    try:
        ports = list(serial.tools.list_ports.comports())
        devices = [{'value': port.device, 'label': port.description if port.description != 'n/a' else port.device} for port in ports]
        return jsonify(devices)
    except (OSError, PermissionError) as e:
        logging.error(f"Error listing serial devices: {e}")
        return jsonify({'error': f'Failed to list serial devices: {str(e)}'}), 500
    except Exception as e:
        logging.error(f"Unexpected error listing serial devices: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@telemetry_bp.route('/baud-rates', methods=['GET'])
def get_baud_rates():
    baud_rates = [
        {'value': 9600, 'label': '9600'},
        {'value': 19200, 'label': '19200'},
        {'value': 38400, 'label': '38400'},
        {'value': 57600, 'label': '57600'},
        {'value': 115200, 'label': '115200'},
        {'value': 230400, 'label': '230400'},
        {'value': 460800, 'label': '460800'},
        {'value': 921600, 'label': '921600'}
    ]
    return jsonify(baud_rates)

@telemetry_bp.route('/mavlink-versions', methods=['GET'])
def get_mavlink_versions():
    mavlink_versions = [
        {'value': 1, 'label': '1.0'},
        {'value': 2, 'label': '2.0'},
        {'value': 3, 'label': '3.0'}
    ]
    return jsonify(mavlink_versions)

@telemetry_bp.route('/udp-destinations', methods=['GET'])
def get_udp_destinations():
    destinations = UdpDestination.query.all()
    return jsonify([{'ip': dest.ip, 'port': dest.port} for dest in destinations])

@telemetry_bp.route('/add-udp-destination', methods=['POST'])
@login_required
def add_udp_destination():
    data = request.json
    ip = data.get('ip')
    port = data.get('port')
    
    # Validate input
    if not ip or port is None:
        return jsonify({'error': 'IP and port are required'}), 400
    
    # Convert port to int if it's a string
    try:
        port = int(port)
    except (ValueError, TypeError):
        return jsonify({'error': 'Port must be a number'}), 400
    
    # Validate UDP destination
    valid, error = validate_udp_destination(ip, port)
    if not valid:
        log_security_event('udp_destination_validation_failed', {
            'ip': ip,
            'port': port,
            'error': error
        }, current_user)
        return jsonify({'error': f'Invalid UDP destination: {error}'}), 400
    
    # Check if destination already exists
    existing = UdpDestination.query.filter_by(ip=ip, port=port).first()
    if existing:
        return jsonify({'error': 'UDP destination already exists'}), 400
    
    new_destination = UdpDestination(ip=ip, port=port)
    db.session.add(new_destination)
    db.session.commit()
    
    log_security_event('udp_destination_added', {
        'ip': ip,
        'port': port
    }, current_user)
    
    return jsonify({"status": "UDP destination added"})

# Remove UDP endpoint
@telemetry_bp.route('/remove-udp-destination', methods=['POST'])
def remove_udp_destination():
    data = request.json
    ip = data.get('ip')
    port = data.get('port')
    destination = UdpDestination.query.filter_by(ip=ip, port=port).first()
    db.session.delete(destination)
    db.session.commit()
    return jsonify({"status": "UDP destination removed"})

@telemetry_bp.route('/set_parameter', methods=['POST'])
@login_required
@rate_limit()
def set_parameter_endpoint():
    data = request.json
    param_id = data.get('param_id')
    param_value = data.get('param_value')

    if not param_id or param_value is None:
        return jsonify({'error': 'Invalid parameter ID or value'}), 400

    # Validate parameter name
    name_valid, name_error = validate_parameter_name(param_id)
    if not name_valid:
        log_security_event('parameter_validation_failed', {
            'param_id': param_id,
            'error': name_error
        }, current_user)
        return jsonify({'error': f'Invalid parameter name: {name_error}'}), 400

    # Validate parameter value
    value_valid, value_error = validate_parameter_value(param_value)
    if not value_valid:
        log_security_event('parameter_validation_failed', {
            'param_id': param_id,
            'param_value': param_value,
            'error': value_error
        }, current_user)
        return jsonify({'error': f'Invalid parameter value: {value_error}'}), 400

    log_security_event('parameter_change_attempt', {
        'param_id': param_id,
        'param_value': param_value
    }, current_user)

    try:
        result = set_parameter(param_id, param_value, user=current_user)
        if result is not None:
            log_security_event('parameter_changed', {
                'param_id': param_id,
                'old_value': None,  # Could be enhanced to track old value
                'new_value': result
            }, current_user)
            return jsonify({'status': 'Parameter set', 'param_id': param_id, 'param_value': result})
        else:
            log_security_event('parameter_change_failed', {
                'param_id': param_id,
                'reason': 'No response from flight controller'
            }, current_user)
            return jsonify({'error': 'Failed to set parameter'}), 500
    except (ConnectionError, TimeoutError) as e:
        log_security_event('parameter_change_failed', {
            'param_id': param_id,
            'error': str(e),
            'error_type': type(e).__name__
        }, current_user)
        return jsonify({'error': f'Connection error: {str(e)}'}), 500
    except Exception as e:
        log_security_event('parameter_change_failed', {
            'param_id': param_id,
            'error': str(e),
            'error_type': type(e).__name__
        }, current_user)
        return jsonify({'error': f'Failed to set parameter: {str(e)}'}), 500