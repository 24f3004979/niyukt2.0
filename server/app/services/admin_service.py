from datetime import datetime

from app.extensions import db
from app.models.user import User
from app.models.drive import Drive


def list_pending_drives():
    return Drive.query.filter_by(status="pending").order_by(Drive.created_at.desc()).all()


def list_all_drives(status=None):
    query = Drive.query
    if status:
        query = query.filter_by(status=status)
    return query.order_by(Drive.created_at.desc()).all()


def approve_drive(drive_id, admin_id):
    drive = Drive.query.get(drive_id)
    if not drive:
        raise ValueError("Drive not found")
    if drive.status != "pending":
        raise ValueError(f"Drive is already {drive.status}")

    drive.status = "approved"
    drive.approved_by = admin_id
    drive.approved_at = datetime.utcnow()
    db.session.commit()
    return drive


def reject_drive(drive_id, admin_id, reason=None):
    drive = Drive.query.get(drive_id)
    if not drive:
        raise ValueError("Drive not found")
    if drive.status != "pending":
        raise ValueError(f"Drive is already {drive.status}")

    drive.status = "rejected"
    drive.approved_by = admin_id
    drive.approved_at = datetime.utcnow()
    drive.rejection_reason = reason
    db.session.commit()
    return drive



def list_pending_companies():
    return User.query.filter_by(role="company", account_status="pending").all()


def approve_company(company_id):
    company = User.query.get(company_id)
    if not company or company.role != "company":
        raise ValueError("Company account not found")
    company.account_status = "active"
    db.session.commit()
    return company


def reject_company(company_id):
    company = User.query.get(company_id)
    if not company or company.role != "company":
        raise ValueError("Company account not found")
    company.account_status = "rejected"
    db.session.commit()
    return company



def get_all_students():
    return User.query.filter_by(role="student").all()


def get_all_companies():
    return User.query.filter_by(role="company").all()



def block_user(user_id):
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")
    if user.role == "admin":
        raise ValueError("Cannot block an admin account")
    user.account_status = "blocked"
    db.session.commit()
    return user


def unblock_user(user_id, restore_status="active"):
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")
    user.account_status = restore_status
    db.session.commit()
    return user
