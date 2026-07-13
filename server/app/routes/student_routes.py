import os

from flask import Blueprint, jsonify, request, send_from_directory, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from app.utils.decorators import role_required
from app.extensions import db
from app.models.user import User
from app.services import drive_service, application_service

student_bp = Blueprint("student", __name__, url_prefix="/api/student")

ALLOWED_RESUME_EXTENSIONS = {"pdf", "doc", "docx"}


def _err(e, code=400):
    return jsonify({"success": False, "error": {"message": str(e)}}), code


def _current_user_id():
    # JWT 'sub' claim is always a string per spec -- cast back to int here,
    # once, so every service function downstream gets a real int.
    return (get_jwt_identity())


def _allowed_resume(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_RESUME_EXTENSIONS


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
    student_id = _current_user_id()
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
    student_id = _current_user_id()
    print(f'Student ID response : {student_id}')
    applications = application_service.get_applications_for_student(student_id)
    return jsonify([a.to_dict() for a in applications])


# ---------------- Resume ----------------

@student_bp.route("/resume", methods=["POST"])
@jwt_required()
@role_required("student")
def upload_resume():
    student_id = _current_user_id()

    if "resume" not in request.files:
        return _err(ValueError("No file provided (expected form field named 'resume')"))

    file = request.files["resume"]
    if file.filename == "":
        return _err(ValueError("No file selected"))
    if not _allowed_resume(file.filename):
        return _err(ValueError("Only PDF, DOC, or DOCX files are allowed"))

    upload_folder = '/home/madhav/workspace/PROJECTS/niyukt2.0/server/uploads'
    os.makedirs(upload_folder, exist_ok=True)

    filename = secure_filename(f"user_{student_id}_{file.filename}")
    file.save(os.path.join(upload_folder, filename))

    user = User.query.get(student_id)
    user.resume_filename = filename
    db.session.commit()

    return jsonify({"success": True, "message": "Resume uploaded", "data": {"resume_filename": filename}})


@student_bp.route("/resume", methods=["GET"])
@jwt_required()
@role_required("student")
def download_own_resume():
    student_id = _current_user_id()
    user = User.query.get(student_id)
    if not user or not user.resume_filename:
        return _err(ValueError("No resume uploaded yet"), 404)

    upload_folder = current_app.config["RESUME_UPLOAD_FOLDER"]
    return send_from_directory(upload_folder, user.resume_filename, as_attachment=True)