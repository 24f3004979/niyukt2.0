from datetime import datetime

from app.extensions import db
from app.models.application import Application, APPLICATION_STATUSES
from app.models.drive import Drive
from app.models.user import User
from app.models.placement_history import PlacementHistory


def apply_to_drive(student_id, drive_id):
    student = User.query.get(student_id)
    if not student or student.role != "student":
        raise ValueError("Only a student account can apply")
    if student.account_status != "active":
        raise ValueError("Student account is not active")

    drive = Drive.query.get(drive_id)
    if not drive:
        raise ValueError("Drive not found")
    if drive.status != "approved":
        raise ValueError("Drive is not open for applications")

    existing = Application.query.filter_by(student_id=student_id, drive_id=drive_id).first()
    if existing:
        raise ValueError("Already applied to this drive")

    application = Application(student_id=student_id, drive_id=drive_id, status="applied")
    db.session.add(application)
    db.session.flush()  # assigns application.id without committing yet

    _log_history(application, drive)

    db.session.commit()
    return application


def get_applications_for_drive(company_id, drive_id):
    """Company-facing: only the owning company can see applicants for a drive."""
    drive = Drive.query.get(drive_id)
    if not drive:
        raise ValueError("Drive not found")
    if drive.company_id != company_id:
        raise PermissionError("This drive does not belong to your company")

    return Application.query.filter_by(drive_id=drive_id).order_by(Application.applied_at.desc()).all()


def get_applications_for_student(student_id):
    return Application.query.filter_by(student_id=student_id).order_by(Application.applied_at.desc()).all()


def update_application_status(application_id, new_status, package_ctc=None, remarks=None):
    if new_status not in APPLICATION_STATUSES:
        raise ValueError(f"Invalid status. Must be one of {APPLICATION_STATUSES}")

    application = Application.query.get(application_id)
    if not application:
        raise ValueError("Application not found")

    application.status = new_status
    application.updated_at = datetime.utcnow()

    drive = Drive.query.get(application.drive_id)
    _log_history(application, drive, package_ctc=package_ctc, remarks=remarks)

    db.session.commit()
    return application


def _log_history(application, drive, package_ctc=None, remarks=None):
    entry = PlacementHistory(
        student_id=application.student_id,
        application_id=application.id,
        drive_id=drive.id,
        company_id=drive.company_id,
        status=application.status,
        package_ctc=package_ctc,
        remarks=remarks,
    )
    db.session.add(entry)
