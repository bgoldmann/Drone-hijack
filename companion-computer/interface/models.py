from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class TelemetryStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(80), nullable=False)
    packets_received = db.Column(db.Integer, default=0)
    vehicle_type = db.Column(db.String(80), nullable=True)
    firmware_version = db.Column(db.String(80), nullable=True)

class VehicleInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_type = db.Column(db.String(80), nullable=False)
    firmware_version = db.Column(db.String(80), nullable=False)

class UdpDestination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(50))
    port = db.Column(db.Integer)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class AuditLog(db.Model):
    """Audit log for security events and operations"""
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    username = db.Column(db.String(64), nullable=True)
    details = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'event_type': self.event_type,
            'user_id': self.user_id,
            'username': self.username,
            'details': self.details
        }


class ProcessTracker(db.Model):
    """Track running processes"""
    id = db.Column(db.Integer, primary_key=True)
    process_name = db.Column(db.String(100), nullable=False)
    pid = db.Column(db.Integer, nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(20), default='running', nullable=False)  # running, stopped, error
    
    def to_dict(self):
        return {
            'id': self.id,
            'process_name': self.process_name,
            'pid': self.pid,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'status': self.status
        }