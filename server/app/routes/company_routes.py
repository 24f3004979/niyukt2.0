from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.utils.decorators import role_required
from app.models.application import Application
from app.services import drive_service, application_service

company_bp = Blueprint("company", __name__, url_prefix="/api/company")


def _err(e, code=400):
    if isinstance(e, PermissionError):
        code = 403
    return jsonify({"success": False, "error": {"message": str(e)}}), code


@company_bp.route("/drives", methods=["POST"])
@jwt_required()
@role_required("company")
def create_drive():
    company_id = get_jwt_identity()
    data = request.get_json() or {}
    try:
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
    """All of the company's drives regardless of status, so they can track pending ones."""
    company_id = get_jwt_identity()
    drives = drive_service.list_drives_for_company(company_id)
    return jsonify([d.to_dict() for d in drives])


@company_bp.route("/drive/<int:drive_id>/applications", methods=["GET"])
@jwt_required()
@role_required("company")
def drive_applications(drive_id):
    company_id = get_jwt_identity()
    try:
        applications = application_service.get_applications_for_drive(company_id, drive_id)
        return jsonify([a.to_dict() for a in applications])
    except (ValueError, PermissionError) as e:
        print(f"applications with given information :{company_id}, with {drive_id}")
        return _err(e)


@company_bp.route("/application/<int:application_id>/status", methods=["PUT"])
@jwt_required()
@role_required("company")
def update_status(application_id):
    company_id = get_jwt_identity()
    data = request.get_json() or {}
    new_status = data.get("status")
    package_ctc = data.get("package_ctc")
    remarks = data.get("remarks")

    application = Application.query.get(application_id)
    if not application:
        return _err(ValueError("Application not found"), 404)
    if application.drive.company_id != company_id:
        return _err(PermissionError("This application does not belong to your drives"))

    try:
        updated = application_service.update_application_status(
            application_id, new_status, package_ctc=package_ctc, remarks=remarks
        )
        return jsonify({"success": True, "message": "Status updated", "data": updated.to_dict()})
    except ValueError as e:
        return _err(e)