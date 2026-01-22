"""
Unit tests for Export API
"""

import pytest
from flask import Flask
from extensions import db
from models import AttackProgress
from routes.export import bp as export_bp

@pytest.fixture
def app():
    """Create test Flask application"""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    app.register_blueprint(export_bp)
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

def test_export_attack_logs_json(client):
    """Test exporting attack logs as JSON"""
    # Create test data
    with client.application.app_context():
        progress = AttackProgress(
            scenario_id='test-scenario',
            user_id='test-user',
            status='completed'
        )
        db.session.add(progress)
        db.session.commit()
    
    response = client.get('/export/attack-logs?format=json')
    assert response.status_code == 200
    assert response.content_type == 'application/json'

def test_export_attack_logs_csv(client):
    """Test exporting attack logs as CSV"""
    response = client.get('/export/attack-logs?format=csv')
    assert response.status_code == 200
    assert 'text/csv' in response.content_type

def test_export_completion_report(client):
    """Test exporting completion report"""
    response = client.get('/export/completion-report?format=json')
    assert response.status_code == 200

def test_export_with_filters(client):
    """Test exporting with filters"""
    response = client.get('/export/attack-logs?format=json&scenario_id=test-scenario&user_id=test-user')
    assert response.status_code == 200
