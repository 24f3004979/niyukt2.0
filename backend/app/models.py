from datetime import datetime
from . import db


class User(db.Model):
    '''
    User core information schema
    id, username, email, password_hash,role
    '''

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255)
    )


    role = db.Column(
        db.String(20),
        default="STUDENT"
    )


class Resume(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    ) # Id refered at application stage for user selection

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

    resume_path = db.Column(
        db.String(255)
    )

    uploaded_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class Drive(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    company_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "company_profile.id"
        )
    )


    title = db.Column(
        db.String(200)
    )


    description = db.Column(
        db.Text
    )


    required_branch = db.Column(
        db.String(100)
    )


    deadline = db.Column(
        db.DateTime
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )



class Application(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    student_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )


    drive_id = db.Column(
        db.Integer,
        db.ForeignKey("drive.id")
    )


    status = db.Column(
        db.String(50),
        default="APPLIED"
    )


    applied_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    # Preventing dublicate application

    __table_args__ = (
        db.UniqueConstraint(
            "student_id",
            "drive_id",
            name="unique_student_drive"
        ),
    )


class StatusHistory(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    application_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "application.id"
        )
    )


    status = db.Column(
        db.String(50)
    )


    comment = db.Column(
        db.Text
    )


    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
