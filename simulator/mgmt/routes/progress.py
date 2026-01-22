# simulator/mgmt/routes/progress.py
from flask import Blueprint, jsonify, request
from datetime import datetime
from extensions import db
from models import AttackProgress
from . import bp

@bp.route("/progress/update", methods=["POST"])
def update_progress():
    """Update attack scenario progress for a user"""
    data = request.json
    scenario_id = data.get("scenario_id")
    user_id = data.get("user_id", "anonymous")
    status = data.get("status", "in_progress")
    
    if not scenario_id:
        return jsonify({"error": "scenario_id is required"}), 400
    
    if status not in ["not_started", "in_progress", "completed"]:
        return jsonify({"error": "Invalid status"}), 400
    
    # Find or create progress record
    progress = AttackProgress.query.filter_by(
        scenario_id=scenario_id,
        user_id=user_id
    ).first()
    
    if not progress:
        progress = AttackProgress(
            scenario_id=scenario_id,
            user_id=user_id,
            status=status
        )
        db.session.add(progress)
    else:
        progress.status = status
        progress.last_updated = datetime.utcnow()
        if status == "in_progress" and progress.started_at is None:
            progress.started_at = datetime.utcnow()
        if status == "completed":
            progress.completion_time = datetime.utcnow()
        progress.attempts += 1
    
    db.session.commit()
    
    return jsonify({
        "status": "updated",
        "progress": {
            "scenario_id": progress.scenario_id,
            "user_id": progress.user_id,
            "status": progress.status,
            "attempts": progress.attempts,
            "completion_time": progress.completion_time.isoformat() if progress.completion_time else None
        }
    })

@bp.route("/progress/user/<user_id>", methods=["GET"])
def get_user_progress(user_id):
    """Get all progress for a specific user"""
    progress_records = AttackProgress.query.filter_by(user_id=user_id).all()
    
    progress_list = []
    for record in progress_records:
        progress_list.append({
            "scenario_id": record.scenario_id,
            "status": record.status,
            "attempts": record.attempts,
            "started_at": record.started_at.isoformat() if record.started_at else None,
            "completion_time": record.completion_time.isoformat() if record.completion_time else None,
            "last_updated": record.last_updated.isoformat() if record.last_updated else None
        })
    
    return jsonify({
        "user_id": user_id,
        "total_scenarios": len(progress_list),
        "completed": len([p for p in progress_list if p["status"] == "completed"]),
        "in_progress": len([p for p in progress_list if p["status"] == "in_progress"]),
        "not_started": len([p for p in progress_list if p["status"] == "not_started"]),
        "progress": progress_list
    })

@bp.route("/progress/stats", methods=["GET"])
def get_progress_stats():
    """Get overall completion statistics"""
    total = AttackProgress.query.count()
    completed = AttackProgress.query.filter_by(status="completed").count()
    in_progress = AttackProgress.query.filter_by(status="in_progress").count()
    not_started = AttackProgress.query.filter_by(status="not_started").count()
    
    # Get most attempted scenarios
    from sqlalchemy import func
    most_attempted = db.session.query(
        AttackProgress.scenario_id,
        func.sum(AttackProgress.attempts).label('total_attempts')
    ).group_by(AttackProgress.scenario_id).order_by(func.sum(AttackProgress.attempts).desc()).limit(10).all()
    
    # Get completion rate by scenario
    completion_by_scenario = db.session.query(
        AttackProgress.scenario_id,
        func.count(AttackProgress.id).label('total'),
        func.sum(func.cast(AttackProgress.status == 'completed', db.Integer)).label('completed')
    ).group_by(AttackProgress.scenario_id).all()
    
    return jsonify({
        "overall": {
            "total": total,
            "completed": completed,
            "in_progress": in_progress,
            "not_started": not_started,
            "completion_rate": (completed / total * 100) if total > 0 else 0
        },
        "most_attempted": [
            {"scenario_id": scenario_id, "total_attempts": attempts}
            for scenario_id, attempts in most_attempted
        ],
        "completion_by_scenario": [
            {
                "scenario_id": scenario_id,
                "total": total_count,
                "completed": completed_count,
                "completion_rate": (completed_count / total_count * 100) if total_count > 0 else 0
            }
            for scenario_id, total_count, completed_count in completion_by_scenario
        ]
    })

@bp.route("/progress/scenario/<scenario_id>", methods=["GET"])
def get_scenario_progress(scenario_id):
    """Get progress for a specific scenario across all users"""
    progress_records = AttackProgress.query.filter_by(scenario_id=scenario_id).all()
    
    progress_list = []
    for record in progress_records:
        progress_list.append({
            "user_id": record.user_id,
            "status": record.status,
            "attempts": record.attempts,
            "started_at": record.started_at.isoformat() if record.started_at else None,
            "completion_time": record.completion_time.isoformat() if record.completion_time else None
        })
    
    return jsonify({
        "scenario_id": scenario_id,
        "total_users": len(progress_list),
        "completed": len([p for p in progress_list if p["status"] == "completed"]),
        "progress": progress_list
    })
