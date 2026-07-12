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
        return {
            "id": self.id,
            "student_id": self.student_id,
            "student_name": self.student.username if self.student else None,
            "drive_id": self.drive_id,
            "status": self.status,
            "applied_at": self.applied_at.isoformat() if self.applied_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
