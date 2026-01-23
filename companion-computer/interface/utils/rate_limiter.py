"""
Rate limiting utilities for flight controller interface
"""
from functools import wraps
from collections import defaultdict
import time
import threading
from flask import request, jsonify
from flask_login import current_user
import logging
from pathlib import Path
import json

# Rate limit storage: {endpoint: {user_id: [(timestamp, count)]}}
_rate_limit_storage = defaultdict(lambda: defaultdict(list))
_rate_limit_lock = defaultdict(lambda: threading.Lock())

CONFIG_FILE = Path("/interface/config.json")

def _load_config():
    """Load configuration from config.json"""
    if CONFIG_FILE.exists():
        try:
            with CONFIG_FILE.open() as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def _get_rate_limit_config(endpoint):
    """Get rate limit configuration for an endpoint"""
    config = _load_config()
    
    if not config.get('enable_rate_limiting', False):
        return None, None  # Rate limiting disabled
    
    # Get endpoint-specific limits or use defaults
    endpoint_configs = {
        'start_telemetry': {
            'max_calls': config.get('max_connection_attempts_per_hour', 5),
            'time_window': 3600  # 1 hour
        },
        'set_parameter': {
            'max_calls': config.get('max_parameter_changes_per_minute', 10),
            'time_window': 60  # 1 minute
        },
        'add_udp_destination': {
            'max_calls': 20,
            'time_window': 60  # 1 minute
        }
    }
    
    if endpoint in endpoint_configs:
        return endpoint_configs[endpoint]['max_calls'], endpoint_configs[endpoint]['time_window']
    
    # Default rate limit
    return config.get('default_rate_limit', 100), 60


def rate_limit(max_calls=None, time_window=None):
    """
    Rate limiting decorator for Flask endpoints
    
    Args:
        max_calls: Maximum number of calls allowed (overrides config)
        time_window: Time window in seconds (overrides config)
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get rate limit config
            endpoint_name = f.__name__
            config_max, config_window = _get_rate_limit_config(endpoint_name)
            
            # Use provided values or config values
            limit_max = max_calls if max_calls is not None else config_max
            limit_window = time_window if time_window is not None else config_window
            
            # If rate limiting is disabled, skip
            if limit_max is None:
                return f(*args, **kwargs)
            
            # Get user identifier
            user_id = 'anonymous'
            if current_user and current_user.is_authenticated:
                user_id = current_user.id if hasattr(current_user, 'id') else current_user.username
            
            # Get current timestamp
            now = time.time()
            
            # Clean old entries and count recent calls
            with _rate_limit_lock[endpoint_name]:
                user_calls = _rate_limit_storage[endpoint_name][user_id]
                
                # Remove calls outside the time window
                user_calls[:] = [ts for ts in user_calls if now - ts < limit_window]
                
                # Check if limit exceeded
                if len(user_calls) >= limit_max:
                    logging.warning({
                        'event': 'rate_limit_exceeded',
                        'endpoint': endpoint_name,
                        'user': user_id,
                        'limit': limit_max,
                        'window': limit_window,
                        'timestamp': now
                    })
                    return jsonify({
                        'error': f'Rate limit exceeded. Maximum {limit_max} calls per {limit_window} seconds allowed.'
                    }), 429
                
                # Add current call
                user_calls.append(now)
            
            # Call the original function
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator
