from flask import Blueprint, jsonify, request
from pathlib import Path
import json
from extensions import db
from models import UdpDestination

config_bp = Blueprint('config', __name__)

CONFIG_FILE = Path("/interface/config.json")
PRESETS_FILE = Path("/interface/config_presets.json")

@config_bp.route('/config', methods=['GET'])
def get_config():
    if CONFIG_FILE.exists():
        with CONFIG_FILE.open() as fp:
            return jsonify(json.load(fp))
    return jsonify({}), 404

@config_bp.route('/config', methods=['POST'])
def update_config():
    data = request.json
    if not CONFIG_FILE.exists():
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        current_config = {}
    else:
        with CONFIG_FILE.open() as fp:
            current_config = json.load(fp)
    
    # Update with new values
    current_config.update(data)
    
    # Validate configuration
    validation_result = validate_config(current_config)
    if not validation_result['valid']:
        return jsonify({'error': 'Invalid configuration', 'details': validation_result['errors']}), 400
    
    # Write updated config
    with CONFIG_FILE.open('w') as fp:
        json.dump(current_config, fp, indent=4)
    
    return jsonify({'status': 'Config updated', 'config': current_config})

def validate_config(config):
    """Validate configuration values"""
    errors = []
    valid = True
    
    # Validate security_level
    if 'security_level' in config:
        if config['security_level'] not in ['low', 'medium', 'high']:
            errors.append("security_level must be 'low', 'medium', or 'high'")
            valid = False
    
    # Validate wifi_encryption
    if 'wifi_encryption' in config:
        if config['wifi_encryption'] not in ['wep', 'wpa2', 'wpa3']:
            errors.append("wifi_encryption must be 'wep', 'wpa2', or 'wpa3'")
            valid = False
    
    # Validate attack_difficulty
    if 'attack_difficulty' in config:
        if config['attack_difficulty'] not in ['beginner', 'intermediate', 'advanced']:
            errors.append("attack_difficulty must be 'beginner', 'intermediate', or 'advanced'")
            valid = False
    
    # Validate drone_model
    if 'drone_model' in config:
        if config['drone_model'] not in ['quadcopter', 'fixed_wing', 'helicopter']:
            errors.append("drone_model must be 'quadcopter', 'fixed_wing', or 'helicopter'")
            valid = False
    
    # Validate numeric fields
    numeric_fields = ['log_retention_days', 'telemetry_rate', 'geofence_radius', 
                      'max_connection_attempts', 'session_timeout', 'connection_timeout_seconds',
                      'max_connection_attempts_per_hour', 'max_parameter_changes_per_minute',
                      'default_rate_limit']
    for field in numeric_fields:
        if field in config:
            try:
                value = int(config[field])
                if value < 0:
                    errors.append(f"{field} must be non-negative")
                    valid = False
                # Specific range validations
                if field == 'connection_timeout_seconds' and (value < 1 or value > 60):
                    errors.append(f"{field} must be between 1 and 60 seconds")
                    valid = False
                if field in ['max_connection_attempts_per_hour', 'max_parameter_changes_per_minute'] and value > 1000:
                    errors.append(f"{field} exceeds maximum value (1000)")
                    valid = False
            except (ValueError, TypeError):
                errors.append(f"{field} must be a number")
                valid = False
    
    # Validate boolean fields
    boolean_fields = ['mavlink_auth', 'enable_logging', 'enable_geofence', 
                     'enable_rate_limiting', 'parameter_access_control', 'enable_audit_logging']
    for field in boolean_fields:
        if field in config:
            if not isinstance(config[field], bool):
                errors.append(f"{field} must be a boolean")
                valid = False
    
    # Validate mavlink_key if mavlink_auth is enabled
    if config.get('mavlink_auth', False):
        mavlink_key = config.get('mavlink_key', '')
        if not mavlink_key or len(mavlink_key) < 8:
            errors.append("mavlink_key must be at least 8 characters when mavlink_auth is enabled")
            valid = False
    
    # Validate critical_parameters is a list
    if 'critical_parameters' in config:
        if not isinstance(config['critical_parameters'], list):
            errors.append("critical_parameters must be a list")
            valid = False
        else:
            # Validate each parameter name
            for param in config['critical_parameters']:
                if not isinstance(param, str) or len(param) > 16:
                    errors.append(f"Invalid parameter name in critical_parameters: {param}")
                    valid = False
    
    return {'valid': valid, 'errors': errors}

@config_bp.route('/config/udp-destinations', methods=['GET'])
def get_udp_destinations():
    destinations = UdpDestination.query.all()
    destination_list = [{'ip': dest.ip, 'port': dest.port} for dest in destinations]
    return jsonify(destination_list)

@config_bp.route('/config/udp-destinations', methods=['POST'])
def add_udp_destination():
    data = request.json
    ip = data.get('ip')
    port = data.get('port')
    destination = UdpDestination(ip=ip, port=port)
    db.session.add(destination)
    db.session.commit()
    return jsonify({'status': 'UDP destination added'})

@config_bp.route('/config/udp-destinations/<int:id>', methods=['DELETE'])
def delete_udp_destination(id):
    destination = UdpDestination.query.get(id)
    if destination:
        db.session.delete(destination)
        db.session.commit()
        return jsonify({'status': 'UDP destination deleted'})
    return jsonify({'error': 'UDP destination not found'}), 404

@config_bp.route('/config/security-level', methods=['POST'])
def set_security_level():
    data = request.json
    level = data.get('level')
    if level not in ['low', 'medium', 'high']:
        return jsonify({'error': 'Invalid security level'}), 400
    
    if CONFIG_FILE.exists():
        with CONFIG_FILE.open() as fp:
            config = json.load(fp)
    else:
        config = {}
    
    config['security_level'] = level
    with CONFIG_FILE.open('w') as fp:
        json.dump(config, fp, indent=4)
    
    return jsonify({'status': 'Security level updated', 'level': level})

@config_bp.route('/config/wifi-mode', methods=['POST'])
def set_wifi_mode():
    data = request.json
    mode = data.get('mode')
    if mode not in ['wep', 'wpa2', 'wpa3']:
        return jsonify({'error': 'Invalid Wi-Fi mode'}), 400
    
    if CONFIG_FILE.exists():
        with CONFIG_FILE.open() as fp:
            config = json.load(fp)
    else:
        config = {}
    
    config['wifi_encryption'] = mode
    with CONFIG_FILE.open('w') as fp:
        json.dump(config, fp, indent=4)
    
    return jsonify({'status': 'Wi-Fi mode updated', 'mode': mode})

@config_bp.route('/config/presets', methods=['GET'])
def get_presets():
    if PRESETS_FILE.exists():
        with PRESETS_FILE.open() as fp:
            presets = json.load(fp)
            # Return preset names and descriptions
            preset_list = []
            for name, preset in presets.items():
                preset_list.append({
                    'name': name,
                    'description': preset.get('description', ''),
                    'security_level': preset.get('security_level', ''),
                    'wifi_encryption': preset.get('wifi_encryption', '')
                })
            return jsonify(preset_list)
    return jsonify([])

@config_bp.route('/config/preset/<name>', methods=['POST'])
def apply_preset(name):
    if not PRESETS_FILE.exists():
        return jsonify({'error': 'Presets file not found'}), 404
    
    with PRESETS_FILE.open() as fp:
        presets = json.load(fp)
    
    if name not in presets:
        return jsonify({'error': f'Preset "{name}" not found'}), 404
    
    preset = presets[name].copy()
    preset.pop('description', None)  # Remove description from config
    
    # Validate preset
    validation_result = validate_config(preset)
    if not validation_result['valid']:
        return jsonify({'error': 'Invalid preset configuration', 'details': validation_result['errors']}), 400
    
    # Apply preset to config
    if CONFIG_FILE.exists():
        with CONFIG_FILE.open() as fp:
            config = json.load(fp)
    else:
        config = {}
    
    config.update(preset)
    
    with CONFIG_FILE.open('w') as fp:
        json.dump(config, fp, indent=4)
    
    return jsonify({'status': f'Preset "{name}" applied', 'config': config})

@config_bp.route('/config/validation', methods=['GET'])
def validate_current_config():
    if not CONFIG_FILE.exists():
        return jsonify({'valid': False, 'error': 'Config file not found'}), 404
    
    with CONFIG_FILE.open() as fp:
        config = json.load(fp)
    
    validation_result = validate_config(config)
    return jsonify(validation_result)