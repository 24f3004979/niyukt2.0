# backend/app/routes/admin_report_routes.py
#
# Add-on routes for reports + analytics. If admin_routes.py already exists
# from the previous milestone, move these functions into that file's
# `admin_bp` instead of registering a second blueprint — keeps everything
# under one /api/admin prefix and one blueprint registration in __init__.py.

from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.utils.decorators import role_required
from app.models.report import Report
from app.services import analytics_service
from app.tasks.report_tasks import generate_monthly_admin_report

admin_report_bp = Blueprint("admin_report_bp", __name__, url_prefix="/api/admin")


@admin_report_bp.route("/analytics", methods=["GET"])
@jwt_required()
@role_required("admin")
def get_analytics():
    months_back = request.args.get("months_back", default=6, type=int)
    data = analytics_service.get_dashboard_analytics(months_back=months_back)
    return jsonify({"success": True, "data": data})


@admin_report_bp.route("/reports", methods=["GET"])
@jwt_required()
@role_required("admin")
def list_reports():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=20, type=int)

    pagination = (
        Report.query.order_by(Report.generated_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return jsonify(
        {
            "success": True,
            "data": {
                "reports": [r.to_dict() for r in pagination.items],
                "page": pagination.page,
                "total_pages": pagination.pages,
                "total": pagination.total,
            },
        }
    )


@admin_report_bp.route("/reports/<int:report_id>/download", methods=["GET"])
@jwt_required()
@role_required("admin")
def download_report(report_id):
    report = Report.query.get(report_id)
    if not report or not report.file_path:
        return jsonify({"success": False, "error": {"message": "Report not found"}}), 404

    return send_file(
        report.file_path,
        mimetype="text/csv",
        as_attachment=True,
        download_name=f"placement_report_{report.period_start}.csv",
    )


@admin_report_bp.route("/reports/generate-now", methods=["POST"])
@jwt_required()
@role_required("admin")
def generate_report_now():
    admin_id = get_jwt_identity()
    task = generate_monthly_admin_report.delay(triggered_by_user_id=admin_id)
    return jsonify({"success": True, "data": {"task_id": task.id}})


@admin_report_bp.route("/reports/task/<task_id>", methods=["GET"])
@jwt_required()
@role_required("admin")
def get_report_task_status(task_id):
    result = celery.AsyncResult(task_id)
    return jsonify(
        {
            "success": True,
            "data": {
                "task_id": task_id,
                "status": result.status,  # PENDING | STARTED | SUCCESS | FAILURE
                "result": result.result if result.successful() else None,
            },
        }
    )