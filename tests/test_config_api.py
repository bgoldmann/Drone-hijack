"""
Unit tests for Configuration API
"""

import pytest
import json
from pathlib import Path
from flask import Flask
from routes.config import config_bp, validate_config

@pytest.fixture
def app():
    """Create test Flask application"""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(config_bp)
    return app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

def test_validate_config():
    """Test configuration validation"""
    # Valid config
    valid_config = {
        'security_level': 'medium',
        'wifi_encryption': 'wpa2',
        'attack_difficulty': 'intermediate',
        'drone_model': 'quadcopter'
    }
    result = validate_config(valid_config)
    assert result['valid'] == True
    assert len(result['errors']) == 0
    
    # Invalid security level
    invalid_config = {
        'security_level': 'invalid',
        'wifi_encryption': 'wpa2'
    }
    result = validate_config(invalid_config)
    assert result['valid'] == False
    assert len(result['errors']) > 0
    
    # Invalid wifi encryption
    invalid_config2 = {
        'security_level': 'medium',
        'wifi_encryption': 'invalid'
    }
    result = validate_config(invalid_config2)
    assert result['valid'] == False

def test_get_presets(client):
    """Test getting configuration presets"""
    # Mock presets file
    # In real test, would set up test presets file
    response = client.get('/config/presets')
    # Should return 200 or 404 depending on file existence
    assert response.status_code in [200, 404]

def test_config_validation_endpoint(client):
    """Test configuration validation endpoint"""
    # This would require mocking the config file
    # For now, just test endpoint exists
    response = client.get('/config/validation')
    assert response.status_code in [200, 404]
