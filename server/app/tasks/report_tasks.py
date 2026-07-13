
import os
from datetime import date
from dateutil.relativedelta import relativedelta
from flask_mail import Message

from app.celery_app import celery  # module-level instance — see celery_app.py
from app.services import report_service
from app.models.report import Report
from app.models.user import User
from app.extensions import db, mail

REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "reports")


@celery.task(bind=True, name="app.tasks.report_tasks.generate_monthly_admin_report")
def generate_monthly_admin_report(self, triggered_by_user_id=None):
    today = date.today()
    period_start = today.replace(day=1) - relativedelta(months=1)
    period_end = today.replace(day=1) - relativedelta(days=1)

    report = Report(
        report_type="monthly_admin",
        period_start=period_start,
        period_end=period_end,
        status="queued",
        generated_by=triggered_by_user_id,
    )
    db.session.add(report)
    db.session.commit()

    try:
        data = report_service.build_admin_report_data(period_start, period_end)
        csv_text = report_service.build_admin_report_csv(data)

        os.makedirs(REPORTS_DIR, exist_ok=True)
        filename = f"monthly_{period_start:%Y_%m}.csv"
        file_path = os.path.join(REPORTS_DIR, filename)
        with open(file_path, "w", newline="") as f:
            f.write(csv_text)

        report.file_path = file_path
        report.status = "completed"
        db.session.commit()

        _email_report_to_admins(csv_text, period_start, period_end)

        return {"report_id": report.id, "status": "completed"}

    except Exception as exc:
        report.status = "failed"
        db.session.commit()
        raise exc


def _email_report_to_admins(csv_text, period_start, period_end):
    admins = User.query.filter_by(role="admin", account_status="active").all()
    if not admins:
        return

    msg = Message(
        subject=f"Placement Portal — Monthly Report ({period_start:%b %Y})",
        recipients=[a.email for a in admins],
        body=(
            f"Attached is the placement report for "
            f"{period_start:%d %b %Y} to {period_end:%d %b %Y}, covering all "
            f"placements, rejections and platform activity for the period."
        ),
    )
    msg.attach(
        f"placement_report_{period_start:%Y_%m}.csv",
        "text/csv",
        csv_text,
    )
    mail.send(msg)