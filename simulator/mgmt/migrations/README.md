# Database Migrations

This directory contains database migration scripts for the simulator management system.

## Migration 001: Add New Tables

Adds three new tables:
- `AttackProgress`: Tracks user progress on attack scenarios
- `ConfigurationHistory`: Logs configuration changes
- `ExploitExecutionLog`: Logs exploit script executions

### Applying Migrations

Since the models are defined in `models.py`, the tables will be created automatically when `db.create_all()` is called.

To manually apply:

```python
from app import create_app
from extensions import db
from models import AttackProgress, ConfigurationHistory, ExploitExecutionLog

app = create_app()
with app.app_context():
    db.create_all()
```

Or if using Flask-Migrate:

```bash
flask db upgrade
```

### Migration Status

- [x] Migration 001: Add new tables (AttackProgress, ConfigurationHistory, ExploitExecutionLog)
