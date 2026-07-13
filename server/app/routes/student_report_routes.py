# backend/app/routes/student_report_routes.py
#
# Add-on route for the student CSV download. If student_routes.py already
# exists from Phase 3, move this function into that file's `student_bp`
# instead of registering a second blueprint.

from flask import Blueprint, Response
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.utils.decorators import role_required  # matches pattern used on admin_bp
from app.services import report_service

student_report_bp = Blueprint("student_report_bp", __name__, url_prefix="/api/students")


@student_report_bp.route("/placement-history/csv", methods=["GET"])
@jwt_required()
@role_required("student")
def download_placement_history_csv():
    student_id = get_jwt_identity()
    csv_text = report_service.build_student_history_csv(student_id)

    return Response(
        csv_text,
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=placement_history.csv"
        },
    )