from datetime import datetime

from app.extensions import db


class PlacementHistory(db.Model):
    """
    Append-only log. A new row is written every time an application's
    status changes (applied -> shortlisted -> interview -> selected/rejected).

    This gives a full audit trail per student without any extra sync
    logic: the "fetcher for an individual student" is just a filtered
    query on this table, and the admin-wide view is the unfiltered one.
    """

    __tablename__ = "placement_history"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    application_id = db.Column(db.Integer, db.ForeignKey("applications.id"), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey("drives.id"), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    status = db.Column(db.String(20), nullable=False)
    package_ctc = db.Column(db.Float, nullable=True)  # filled in once status == "selected"

    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship("User", foreign_keys=[student_id])
    company = db.relationship("User", foreign_keys=[company_id])

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "student_name": self.student.username if self.student else None,
            "application_id": self.application_id,
            "drive_id": self.drive_id,
            "company_id": self.company_id,
            "company_name": self.company.username if self.company else None,
            "status": self.status,
            "package_ctc": self.package_ctc,
            "remarks": self.remarks,
            "recorded_at": self.recorded_at.isoformat() if self.recorded_at else None,
        }

