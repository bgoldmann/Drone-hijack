from extensions import db
from datetime import datetime

STATUS_CHOICES = ['Disabled', 'Enabled', 'Loading', 'Active']

class Stage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(db.String(50), default='Disabled')

    def __repr__(self):
        return f'<Stage {self.name}, Status {self.status}>'

    @db.validates('status')
    def validate_status(self, key, status):
        if status not in STATUS_CHOICES:
            raise ValueError("Invalid status")
        return status

def create_initial_stages():

    stage_names = ["Stage 1", "Stage 2", "Stage 3", "Stage 4", "Stage 5", "Stage 6"]
    for name in stage_names:
        if not Stage.query.filter_by(name=name).first():
            if name == "Stage 1":
                stage = Stage(name=name, code=name.replace(" ", "").lower(), status="Enabled")
            else:
                stage = Stage(name=name, code=name.replace(" ", "").lower(), status="Disabled")
            db.session.add(stage)
        # Else update the status of all stages (except Stage 1 which should be enabled) to Disabled
        else:
            stage = Stage.query.filter_by(name=name).first()
            if name == "Stage 1":
                stage.status = "Enabled"
            else:
                stage.status = "Disabled"

    db.session.commit()

class AttackProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scenario_id = db.Column(db.String(100), nullable=False, index=True)
    user_id = db.Column(db.String(100), nullable=False, index=True)
    status = db.Column(db.String(50), nullable=False, default='not_started')  # not_started, in_progress, completed
    completion_time = db.Column(db.DateTime, nullable=True)
    attempts = db.Column(db.Integer, default=0)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<AttackProgress {self.scenario_id} - {self.user_id}: {self.status}>'

class ConfigurationHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    config_key = db.Column(db.String(100), nullable=False)
    old_value = db.Column(db.Text, nullable=True)
    new_value = db.Column(db.Text, nullable=False)
    changed_by = db.Column(db.String(100), nullable=True)
    changed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ConfigurationHistory {self.config_key} changed at {self.changed_at}>'

class ExploitExecutionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    execution_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    scenario_id = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), nullable=False)  # pending, running, completed, failed
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    output = db.Column(db.Text, nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<ExploitExecutionLog {self.execution_id}: {self.status}>'