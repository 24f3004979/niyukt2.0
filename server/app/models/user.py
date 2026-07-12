from app.extensions import db


class User(db.Model):
    ''' id, email, username, password, role, account_status '''
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True
    )
    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False,
        index=True
    )
    password = db.Column(
        db.String(255),
        nullable=False
    )
    role = db.Column(
        db.String(50),
        default="student"
    )
    account_status = db.Column(
        db.String(50),
        default="active"
    )
    def serialize(self):

        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "role": self.role,
            "account_status": self.account_status
        }
