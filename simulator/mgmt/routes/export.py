# simulator/mgmt/routes/export.py
from flask import Blueprint, jsonify, request, send_file, Response
from datetime import datetime, timedelta
import json
import csv
import io
from extensions import db
from models import AttackProgress, ExploitExecutionLog
from . import bp

@bp.route("/export/attack-logs", methods=["GET"])
def export_attack_logs():
    """Export attack logs as JSON or CSV"""
    format_type = request.args.get("format", "json")  # json or csv
    scenario_id = request.args.get("scenario_id", None)
    user_id = request.args.get("user_id", None)
    start_date = request.args.get("start_date", None)
    end_date = request.args.get("end_date", None)
    
    # Build query
    query = AttackProgress.query
    
    if scenario_id:
        query = query.filter_by(scenario_id=scenario_id)
    if user_id:
        query = query.filter_by(user_id=user_id)
    if start_date:
        try:
            start = datetime.fromisoformat(start_date)
            query = query.filter(AttackProgress.started_at >= start)
        except ValueError:
            pass
    if end_date:
        try:
            end = datetime.fromisoformat(end_date)
            query = query.filter(AttackProgress.started_at <= end)
        except ValueError:
            pass
    
    records = query.all()
    
    if format_type == "json":
        data = []
        for record in records:
            data.append({
                "scenario_id": record.scenario_id,
                "user_id": record.user_id,
                "status": record.status,
                "attempts": record.attempts,
                "started_at": record.started_at.isoformat() if record.started_at else None,
                "completion_time": record.completion_time.isoformat() if record.completion_time else None,
                "last_updated": record.last_updated.isoformat() if record.last_updated else None
            })
        
        output = io.BytesIO()
        output.write(json.dumps(data, indent=2).encode('utf-8'))
        output.seek(0)
        
        filename = f"attack_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        return send_file(
            output,
            mimetype='application/json',
            as_attachment=True,
            download_name=filename
        )
    
    elif format_type == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            "scenario_id", "user_id", "status", "attempts",
            "started_at", "completion_time", "last_updated"
        ])
        
        # Write data
        for record in records:
            writer.writerow([
                record.scenario_id,
                record.user_id,
                record.status,
                record.attempts,
                record.started_at.isoformat() if record.started_at else "",
                record.completion_time.isoformat() if record.completion_time else "",
                record.last_updated.isoformat() if record.last_updated else ""
            ])
        
        output.seek(0)
        filename = f"attack_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={
                'Content-Disposition': f'attachment; filename={filename}'
            }
        )
    
    return jsonify({"error": "Invalid format. Use 'json' or 'csv'"}), 400

@bp.route("/export/completion-report", methods=["GET"])
def export_completion_report():
    """Export scenario completion report"""
    user_id = request.args.get("user_id", None)
    format_type = request.args.get("format", "json")
    
    if user_id:
        progress_records = AttackProgress.query.filter_by(user_id=user_id).all()
    else:
        # Get all unique scenarios and their completion stats
        from sqlalchemy import func
        progress_records = db.session.query(
            AttackProgress.scenario_id,
            func.count(AttackProgress.id).label('total'),
            func.sum(func.cast(AttackProgress.status == 'completed', db.Integer)).label('completed'),
            func.avg(AttackProgress.attempts).label('avg_attempts')
        ).group_by(AttackProgress.scenario_id).all()
        
        report_data = []
        for scenario_id, total, completed, avg_attempts in progress_records:
            report_data.append({
                "scenario_id": scenario_id,
                "total_attempts": total,
                "completed": completed,
                "completion_rate": (completed / total * 100) if total > 0 else 0,
                "average_attempts": float(avg_attempts) if avg_attempts else 0
            })
        
        if format_type == "json":
            output = io.BytesIO()
            output.write(json.dumps(report_data, indent=2).encode('utf-8'))
            output.seek(0)
            filename = f"completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            return send_file(
                output,
                mimetype='application/json',
                as_attachment=True,
                download_name=filename
            )
        else:  # csv
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["scenario_id", "total_attempts", "completed", "completion_rate", "average_attempts"])
            for item in report_data:
                writer.writerow([
                    item["scenario_id"],
                    item["total_attempts"],
                    item["completed"],
                    f"{item['completion_rate']:.2f}%",
                    f"{item['average_attempts']:.2f}"
                ])
            output.seek(0)
            filename = f"completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            return Response(
                output.getvalue(),
                mimetype='text/csv',
                headers={'Content-Disposition': f'attachment; filename={filename}'}
            )
    
    # User-specific report
    report_data = []
    for record in progress_records:
        report_data.append({
            "scenario_id": record.scenario_id,
            "status": record.status,
            "attempts": record.attempts,
            "started_at": record.started_at.isoformat() if record.started_at else None,
            "completion_time": record.completion_time.isoformat() if record.completion_time else None
        })
    
    if format_type == "json":
        output = io.BytesIO()
        output.write(json.dumps(report_data, indent=2).encode('utf-8'))
        output.seek(0)
        filename = f"completion_report_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        return send_file(
            output,
            mimetype='application/json',
            as_attachment=True,
            download_name=filename
        )
    else:  # csv
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["scenario_id", "status", "attempts", "started_at", "completion_time"])
        for item in report_data:
            writer.writerow([
                item["scenario_id"],
                item["status"],
                item["attempts"],
                item["started_at"] or "",
                item["completion_time"] or ""
            ])
        output.seek(0)
        filename = f"completion_report_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )

@bp.route("/export/telemetry", methods=["GET"])
def export_telemetry():
    """Export telemetry data during attacks"""
    scenario_id = request.args.get("scenario_id", None)
    execution_id = request.args.get("execution_id", None)
    format_type = request.args.get("format", "json")
    
    # This would integrate with actual telemetry collection
    # For now, return a placeholder structure
    telemetry_data = {
        "scenario_id": scenario_id,
        "execution_id": execution_id,
        "timestamp": datetime.now().isoformat(),
        "note": "Telemetry export functionality requires integration with telemetry collection system"
    }
    
    if format_type == "json":
        output = io.BytesIO()
        output.write(json.dumps(telemetry_data, indent=2).encode('utf-8'))
        output.seek(0)
        filename = f"telemetry_{scenario_id or 'all'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        return send_file(
            output,
            mimetype='application/json',
            as_attachment=True,
            download_name=filename
        )
    else:  # csv
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["scenario_id", "execution_id", "timestamp", "note"])
        writer.writerow([
            telemetry_data["scenario_id"],
            telemetry_data["execution_id"],
            telemetry_data["timestamp"],
            telemetry_data["note"]
        ])
        output.seek(0)
        filename = f"telemetry_{scenario_id or 'all'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )

@bp.route("/export/exploit-executions", methods=["GET"])
def export_exploit_executions():
    """Export exploit execution logs"""
    format_type = request.args.get("format", "json")
    status = request.args.get("status", None)
    
    query = ExploitExecutionLog.query
    if status:
        query = query.filter_by(status=status)
    
    records = query.order_by(ExploitExecutionLog.started_at.desc()).all()
    
    data = []
    for record in records:
        data.append({
            "execution_id": record.execution_id,
            "scenario_id": record.scenario_id,
            "user_id": record.user_id,
            "status": record.status,
            "started_at": record.started_at.isoformat() if record.started_at else None,
            "completed_at": record.completed_at.isoformat() if record.completed_at else None,
            "error_message": record.error_message
        })
    
    if format_type == "json":
        output = io.BytesIO()
        output.write(json.dumps(data, indent=2).encode('utf-8'))
        output.seek(0)
        filename = f"exploit_executions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        return send_file(
            output,
            mimetype='application/json',
            as_attachment=True,
            download_name=filename
        )
    else:  # csv
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["execution_id", "scenario_id", "user_id", "status", "started_at", "completed_at", "error_message"])
        for item in data:
            writer.writerow([
                item["execution_id"],
                item["scenario_id"],
                item["user_id"],
                item["status"],
                item["started_at"] or "",
                item["completed_at"] or "",
                item["error_message"] or ""
            ])
        output.seek(0)
        filename = f"exploit_executions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )
