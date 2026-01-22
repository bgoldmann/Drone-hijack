"""
Database Migration: Add new tables for attack progress, configuration history, and exploit execution logs

Run this migration with:
    python -c "from app import create_app; from extensions import db; from models import AttackProgress, ConfigurationHistory, ExploitExecutionLog; app = create_app(); app.app_context().push(); db.create_all()"
"""

# This migration adds the following tables:
# - AttackProgress: Tracks user progress on attack scenarios
# - ConfigurationHistory: Logs configuration changes
# - ExploitExecutionLog: Logs exploit script executions

# The models are already defined in models.py, so running db.create_all() will create these tables
# This file serves as documentation of the migration

MIGRATION_NOTES = """
Migration 001: Add New Tables

Tables Added:
1. AttackProgress
   - id (Integer, Primary Key)
   - scenario_id (String, Indexed)
   - user_id (String, Indexed)
   - status (String: not_started, in_progress, completed)
   - completion_time (DateTime, Nullable)
   - attempts (Integer, Default: 0)
   - started_at (DateTime)
   - last_updated (DateTime)

2. ConfigurationHistory
   - id (Integer, Primary Key)
   - config_key (String)
   - old_value (Text, Nullable)
   - new_value (Text)
   - changed_by (String, Nullable)
   - changed_at (DateTime)

3. ExploitExecutionLog
   - id (Integer, Primary Key)
   - execution_id (String, Unique, Indexed)
   - scenario_id (String)
   - user_id (String, Nullable)
   - status (String: pending, running, completed, failed)
   - started_at (DateTime)
   - completed_at (DateTime, Nullable)
   - output (Text, Nullable)
   - error_message (Text, Nullable)

To apply this migration:
1. Ensure models.py contains the new model definitions
2. Run: python -c "from app import create_app; from extensions import db; app = create_app(); app.app_context().push(); db.create_all()"
3. Or use Flask-Migrate if available: flask db upgrade
"""
