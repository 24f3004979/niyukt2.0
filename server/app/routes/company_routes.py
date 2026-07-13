from flask import Blueprint, request, jsonify, send_from_directory, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.utils.decorators import role_required
from app.models.application import Application
from app.services import drive_service, application_service

company_bp = Blueprint("company", __name__, url_prefix="/api/company")


def _err(e, code=400):
    if isinstance(e, PermissionError):
        code = 403
    return jsonify({"success": False, "error": {"message": str(e)}}), code


def _current_user_id():
    # JWT 'sub' claim is always a string per spec -- cast back to int here,
    # once, so every service function downstream gets a real int. Without
    # this, "drive.company_id != company_id" silently fails (int vs str)
    # and every ownership check -- including "list my applications" -- breaks.
    return int(get_jwt_identity())


@company_bp.route("/drives", methods=["POST"])
@jwt_required()
@role_required("company")
def create_drive():
    company_id = _current_user_id()
    data = request.get_json() or {}
    try:
        print(f'Drive creation data : {data}')
        drive = drive_service.create_drive(company_id, data)
        return jsonify({
            "success": True, "message": "Drive submitted for admin approval",
            "data": drive.to_dict(),
        }), 201
    except ValueError as e:
        return _err(e)


@company_bp.route("/drives", methods=["GET"])
@jwt_required()
@role_required("company")
def my_drives():
    company_id = _current_user_id()
    drives = drive_service.list_drives_for_company(company_id)
    return jsonify([d.to_dict() for d in drives])


@company_bp.route("/drive/<int:drive_id>/applications", methods=["GET"])
@jwt_required()
@role_required("company")
def drive_applications(drive_id):
    company_id = _current_user_id()
    try:
        applications = application_service.get_applications_for_drive(company_id, drive_id)
        return jsonify([a.to_dict() for a in applications])
    except (ValueError, PermissionError) as e:
        return _err(e)


@company_bp.route("/applications", methods=["GET"])
@jwt_required()
@role_required("company")
def all_applications():
    """Every applicant across every drive this company has posted."""
    company_id = _current_user_id()
    applications = application_service.get_applications_for_company(company_id)
    return jsonify([a.to_dict() for a in applications])


@company_bp.route("/application/<int:application_id>/status", methods=["PUT"])
@jwt_required()
@role_required("company")
def update_status(application_id):
    company_id = _current_user_id()
    data = request.get_json() or {}
    new_status = data.get("status")

    application = Application.query.get(application_id)
    if not application:
        return _err(ValueError("Application not found"), 404)
    if application.drive.company_id != company_id:
        return _err(PermissionError("This application does not belong to your drives"))

    try:
        updated = application_service.update_application_status(application_id, new_status)
        return jsonify({"success": True, "message": "Status updated", "data": updated.to_dict()})
    except ValueError as e:
        return _err(e)


@company_bp.route("/application/<int:application_id>/resume", methods=["GET"])
@jwt_required()
@role_required("company")
def download_applicant_resume(application_id):
    company_id = _current_user_id()

    application = Application.query.get(application_id)
    if not application:
        return _err(ValueError("Application not found"), 404)
    if application.drive.company_id != company_id:
        return _err(PermissionError("This application does not belong to your drives"))

    student = application.student
    if not student or not student.resume_filename:
        return _err(ValueError("This applicant has not uploaded a resume"), 404)
    
    upload_folder = '/home/madhav/workspace/PROJECTS/niyukt2.0/server/uploads'
    return send_from_directory(upload_folder, student.resume_filename, as_attachment=True)