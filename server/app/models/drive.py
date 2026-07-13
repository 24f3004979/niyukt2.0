from datetime import datetime

from app.extensions import db


class Drive(db.Model):
    __tablename__ = "drives"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    package_ctc = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(20), nullable=False, default="pending")  # pending | approved | rejected
    created_at = db.Column(db.DateTime, default=datetime.now)

    company = db.relationship("User", foreign_keys=[company_id])

    def to_dict(self):
        return {
            "id": self.id,
            "company_id": self.company_id,
            "company_name": self.company.username if self.company else None,
            "title": self.title,
            "description": self.description,
            "package_ctc": self.package_ctc,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }