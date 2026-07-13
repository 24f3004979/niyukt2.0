from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


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
    resume_filename = db.Column(
        db.String(50),
        default=""
    )
    def serialize(self):

        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "role": self.role,
            "account_status": self.account_status
        }
    
    def set_password(self, password):
        print(f"User password : {password}")
        self.password = generate_password_hash(
            password
        )
    def check_password_hash(self, password):
        ''' Checking password hash for the final checkout'''

        print(f"Password Check is being running")
        return check_password_hash(
            self.password, password
        )

