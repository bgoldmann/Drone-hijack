"""
Unit tests for Progress Tracking API
"""

import pytest
from flask import Flask
from extensions import db
from models import AttackProgress
from routes.progress import bp as progress_bp

@pytest.fixture
def app():
    """Create test Flask application"""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    app.register_blueprint(progress_bp)
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

def test_update_progress(client):
    """Test updating attack progress"""
    response = client.post('/progress/update', json={
        'scenario_id': 'test-scenario',
        'user_id': 'test-user',
        'status': 'in_progress'
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'updated'
    assert data['progress']['scenario_id'] == 'test-scenario'
    assert data['progress']['status'] == 'in_progress'

def test_get_user_progress(client):
    """Test getting user progress"""
    # Create some progress records
    with client.application.app_context():
        progress1 = AttackProgress(
            scenario_id='scenario1',
            user_id='test-user',
            status='completed'
        )
        progress2 = AttackProgress(
            scenario_id='scenario2',
            user_id='test-user',
            status='in_progress'
        )
        db.session.add(progress1)
        db.session.add(progress2)
        db.session.commit()
    
    response = client.get('/progress/user/test-user')
    assert response.status_code == 200
    data = response.get_json()
    assert data['user_id'] == 'test-user'
    assert data['total_scenarios'] == 2
    assert data['completed'] == 1
    assert data['in_progress'] == 1

def test_get_progress_stats(client):
    """Test getting progress statistics"""
    # Create test data
    with client.application.app_context():
        for i in range(5):
            progress = AttackProgress(
                scenario_id=f'scenario{i}',
                user_id='test-user',
                status='completed' if i < 3 else 'in_progress'
            )
            db.session.add(progress)
        db.session.commit()
    
    response = client.get('/progress/stats')
    assert response.status_code == 200
    data = response.get_json()
    assert 'overall' in data
    assert data['overall']['total'] == 5
