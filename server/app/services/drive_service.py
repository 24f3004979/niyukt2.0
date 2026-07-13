from app.extensions import db
from app.models.drive import Drive
from app.models.user import User


def create_drive(company_id, data):
    company = User.query.get(company_id)
    if not company or company.role != "company":
        raise ValueError("Only a company account can create a drive")
    if company.account_status != "active":
        raise ValueError("Company account is not active")

    drive = Drive(
        company_id=company_id,
        title=data.get("title"),
        description=data.get("description"),
        role_offered=data.get("role_offered"),
        package_ctc=data.get("package_ctc"),
        status="pending",  # always starts pending, admin must approve
    )
    db.session.add(drive)
    db.session.commit()
    return drive


def get_drive(drive_id):
    return Drive.query.get(drive_id)


def list_drives(status=None):
    query = Drive.query
    if status:
        query = query.filter_by(status=status)
    return query.order_by(Drive.created_at.desc()).all()


def list_drives_for_company(company_id):
    return Drive.query.filter_by(company_id=company_id).order_by(Drive.created_at.desc()).all()
