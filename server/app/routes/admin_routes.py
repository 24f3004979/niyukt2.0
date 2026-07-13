from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.utils.decorators import role_required
from app.services import admin_service

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


def _err(e, code=400):
    return jsonify({"success": False, "error": {"message": str(e)}}), code


# ---------------- Drives ----------------

@admin_bp.route("/drives/pending", methods=["GET"])
@jwt_required()
@role_required("admin")
def pending_drives():
    drives = admin_service.list_pending_drives()
    return jsonify([d.to_dict() for d in drives])


@admin_bp.route("/drives", methods=["GET"])
@jwt_required()
@role_required("admin")
def all_drives():
    status = request.args.get("status")  # ?status=approved / pending / rejected
    drives = admin_service.list_all_drives(status=status)
    return jsonify([d.to_dict() for d in drives])


@admin_bp.route("/drive/<int:drive_id>/approve", methods=["PUT"])
@jwt_required()
@role_required("admin")
def approve_drive(drive_id):
    try:
        drive = admin_service.approve_drive(drive_id)
        return jsonify({"success": True, "message": "Drive approved", "data": drive.to_dict()})
    except ValueError as e:
        return _err(e)


@admin_bp.route("/drive/<int:drive_id>/reject", methods=["PUT"])
@jwt_required()
@role_required("admin")
def reject_drive(drive_id):
    try:
        drive = admin_service.reject_drive(drive_id)
        return jsonify({"success": True, "message": "Drive rejected", "data": drive.to_dict()})
    except ValueError as e:
        return _err(e)


# ---------------- Company approval ----------------

@admin_bp.route("/companies/pending", methods=["GET"])
@jwt_required()
@role_required("admin")
def pending_companies():
    companies = admin_service.list_pending_companies()
    return jsonify([{"id": c.id, "username": c.username, "email": c.email} for c in companies])


@admin_bp.route("/company/<int:company_id>/approve", methods=["PUT"])
@jwt_required()
@role_required("admin")
def approve_company(company_id):
    try:
        company = admin_service.approve_company(company_id)
        return jsonify({
            "success": True, "message": "Company approved",
            "data": {"id": company.id, "status": company.account_status},
        })
    except ValueError as e:
        return _err(e)


@admin_bp.route("/company/<int:company_id>/reject", methods=["PUT"])
@jwt_required()
@role_required("admin")
def reject_company(company_id):
    try:
        company = admin_service.reject_company(company_id)
        return jsonify({
            "success": True, "message": "Company rejected",
            "data": {"id": company.id, "status": company.account_status},
        })
    except ValueError as e:
        return _err(e)


# ---------------- Users ----------------

@admin_bp.route("/students", methods=["GET"])
@jwt_required()
@role_required("admin")
def all_students():
    students = admin_service.get_all_students()
    return jsonify([
        {"id": s.id, "username": s.username, "email": s.email, "account_status": s.account_status}
        for s in students
    ])


@admin_bp.route("/companies", methods=["GET"])
@jwt_required()
@role_required("admin")
def all_companies():
    companies = admin_service.get_all_companies()
    return jsonify([
        {"id": c.id, "username": c.username, "email": c.email, "account_status": c.account_status}
        for c in companies
    ])


@admin_bp.route("/user/<int:user_id>/block", methods=["PUT"])
@jwt_required()
@role_required("admin")
def block_user(user_id):
    try:
        user = admin_service.block_user(user_id)
        return jsonify({
            "success": True, "message": "User blocked",
            "data": {"id": user.id, "status": user.account_status},
        })
    except ValueError as e:
        return _err(e)


@admin_bp.route("/user/<int:user_id>/unblock", methods=["PUT"])
@jwt_required()
@role_required("admin")
def unblock_user(user_id):
    try:
        user = admin_service.unblock_user(user_id)
        return jsonify({
            "success": True, "message": "User unblocked",
            "data": {"id": user.id, "status": user.account_status},
        })
    except ValueError as e:
        return _err(e)