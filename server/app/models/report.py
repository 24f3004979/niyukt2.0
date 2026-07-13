# backend/app/models/report.py
#
# Assumes the shared `db` SQLAlchemy instance lives in app/extensions.py,
# matching the pattern used by Drive / Application / PlacementHistory.
# Remember to import and register this model in models/__init__.py.

from datetime import datetime
from app.extensions import db


class Report(db.Model):
    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True)

    # "monthly_admin" today; leaves room for other report types later
    # (e.g. "student_export") without a schema change.
    report_type = db.Column(db.String(50), nullable=False, default="monthly_admin")

    period_start = db.Column(db.Date, nullable=False)
    period_end = db.Column(db.Date, nullable=False)

    file_path = db.Column(db.String(255), nullable=True)

    status = db.Column(db.String(20), nullable=False, default="queued")
    # queued | completed | failed

    generated_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "report_type": self.report_type,
            "period_start": self.period_start.isoformat() if self.period_start else None,
            "period_end": self.period_end.isoformat() if self.period_end else None,
            "status": self.status,
            "generated_by": self.generated_by,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
        }