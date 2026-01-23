"""
Health check endpoints for flight controller monitoring
"""
from flask import Blueprint, jsonify
from flask_login import login_required
from mavlink_connection import connection_state
import subprocess
import logging
import time

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
@login_required
def health_check():
    """
    Health check endpoint
    
    Returns:
        JSON with health status of:
        - MAVLink connection
        - mavlink-routerd process
        - Overall system health
    """
    health_status = {
        'status': 'healthy',
        'timestamp': time.time(),
        'components': {}
    }
    
    # Check MAVLink connection
    mavlink_status = connection_state.get('status', 'unknown')
    last_heartbeat = connection_state.get('last_heartbeat')
    
    health_status['components']['mavlink'] = {
        'status': mavlink_status,
        'last_heartbeat': last_heartbeat,
        'healthy': mavlink_status == 'connected'
    }
    
    if mavlink_status != 'connected':
        health_status['status'] = 'degraded'
    
    # Check mavlink-routerd process
    try:
        # Use pgrep to find mavlink-routerd processes
        result = subprocess.run(
            ["pgrep", "-f", "mavlink-routerd"],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            pids = [int(pid) for pid in result.stdout.strip().split('\n') if pid]
        else:
            pids = []
        process_running = len(pids) > 0
        
        health_status['components']['mavlink_routerd'] = {
            'status': 'running' if process_running else 'stopped',
            'pids': pids,
            'healthy': process_running
        }
        
        if not process_running:
            health_status['status'] = 'degraded'
    except (subprocess.CalledProcessError, ValueError, OSError) as e:
        logging.error(f"Error checking mavlink-routerd process: {e}")
        health_status['components']['mavlink_routerd'] = {
            'status': 'error',
            'error': str(e),
            'healthy': False
        }
        health_status['status'] = 'unhealthy'
    except Exception as e:
        logging.error(f"Unexpected error checking mavlink-routerd process: {e}")
        health_status['components']['mavlink_routerd'] = {
            'status': 'error',
            'error': 'An unexpected error occurred',
            'healthy': False
        }
        health_status['status'] = 'unhealthy'
    
    # Determine overall status
    all_healthy = all(
        comp.get('healthy', False) 
        for comp in health_status['components'].values()
    )
    
    if not all_healthy and health_status['status'] == 'healthy':
        health_status['status'] = 'degraded'
    
    # Return appropriate HTTP status
    status_code = 200
    if health_status['status'] == 'unhealthy':
        status_code = 503
    elif health_status['status'] == 'degraded':
        status_code = 200  # Still return 200 but indicate degraded
    
    return jsonify(health_status), status_code


@health_bp.route('/health/mavlink', methods=['GET'])
@login_required
def mavlink_health():
    """Get MAVLink connection health status"""
    return jsonify({
        'status': connection_state.get('status', 'unknown'),
        'last_heartbeat': connection_state.get('last_heartbeat'),
        'healthy': connection_state.get('status') == 'connected'
    })


@health_bp.route('/health/processes', methods=['GET'])
@login_required
def processes_health():
    """Get process health status"""
    try:
        result = subprocess.run(
            ["pgrep", "-f", "mavlink-routerd"],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            pids = [int(pid) for pid in result.stdout.strip().split('\n') if pid]
        else:
            pids = []
        return jsonify({
            'mavlink_routerd': {
                'running': len(pids) > 0,
                'pids': pids,
                'count': len(pids)
            }
        })
    except (subprocess.CalledProcessError, ValueError, OSError) as e:
        logging.error(f"Error checking processes: {e}")
        return jsonify({
            'error': str(e),
            'mavlink_routerd': {
                'running': False,
                'pids': [],
                'count': 0
            }
        }), 500
    except Exception as e:
        logging.error(f"Unexpected error checking processes: {e}")
        return jsonify({
            'error': 'An unexpected error occurred',
            'mavlink_routerd': {
                'running': False,
                'pids': [],
                'count': 0
            }
        }), 500
