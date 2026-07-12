from datetime import datetime

from app.extensions import db


class Drive(db.Model):
    __tablename__ = "drives"

    id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    role_offered = db.Column(db.String(150), nullable=True)
    package_ctc = db.Column(db.Float, nullable=True)

    # pending -> approved / rejected (admin decides). approved drives can later be closed.
    status = db.Column(db.String(20), nullable=False, default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime, nullable=True)


    def to_dict(self):
        return {
            "id": self.id,
            "company_id": self.company_id,
            "title": self.title,
            "description": self.description,
            "role_offered": self.role_offered,
            "package_ctc": self.package_ctc,
            "status": self.status,
            "created_at":self.created_at,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
        }
