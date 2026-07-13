from datetime import datetime

from app.extensions import db

APPLICATION_STATUSES = ["applied", "shortlisted", "interview", "selected", "rejected"]


class Application(db.Model):
    __tablename__ = "applications"
    __table_args__ = (
        db.UniqueConstraint("student_id", "drive_id", name="uq_student_drive"),
    )

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey("drives.id"), nullable=False)

    status = db.Column(db.String(20), nullable=False, default="applied")

    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = db.relationship("User", foreign_keys=[student_id], backref="applications")

    def to_dict(self):
        # self.drive comes from the backref defined on Drive.applications
        drive = self.drive
        return {
            "id": self.id,
            "student_id": self.student_id,
            "student_name": self.student.username if self.student else None,
            "drive_id": self.drive_id,
            "drive_title": drive.title if drive else None,
            "company_id": drive.company_id if drive else None,
            "company_name": drive.company.username if drive and drive.company else None,
            "package_ctc": drive.package_ctc if drive else None,
            "status": self.status,
            "applied_at": self.applied_at.isoformat() if self.applied_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }