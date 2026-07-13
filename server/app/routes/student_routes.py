from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.utils.decorators import role_required
from app.services import drive_service, application_service, placement_service

student_bp = Blueprint("student", __name__, url_prefix="/api/student")


def _err(e, code=400):
    return jsonify({"success": False, "error": {"message": str(e)}}), code


@student_bp.route("/drives", methods=["GET"])
@jwt_required()
@role_required("student")
def open_drives():
    """Only admin-approved drives are visible to students."""
    drives = drive_service.list_drives(status="approved")
    return jsonify([d.to_dict() for d in drives])


@student_bp.route("/drive/<int:drive_id>/apply", methods=["POST"])
@jwt_required()
@role_required("student")
def apply(drive_id):
    student_id = get_jwt_identity()
    try:
        application = application_service.apply_to_drive(student_id, drive_id)
        return jsonify({
            "success": True, "message": "Applied successfully",
            "data": application.to_dict(),
        }), 201
    except ValueError as e:
        return _err(e)


@student_bp.route("/applications", methods=["GET"])
@jwt_required()
@role_required("student")
def my_applications():
    student_id = get_jwt_identity()
    applications = application_service.get_applications_for_student(student_id)
    return jsonify([a.to_dict() for a in applications])


@student_bp.route("/placement-history", methods=["GET"])
@jwt_required()
@role_required("student")
def my_placement_history():
    student_id = get_jwt_identity()
    history = placement_service.get_history_for_student(student_id)
    return jsonify([h.to_dict() for h in history])