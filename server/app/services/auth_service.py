from app.models.user import User
from app.extensions import db



def register_user(data):

    user = User(
        email=data["email"],
        username=data["username"],
        role=data.get(
            "role",
            "student"
        )
    )


    user.set_password(
        data["password"]
    )


    db.session.add(user)
    db.session.commit()


    return user



def authenticate(username,password):

    user = User.query.filter_by(
        username=username
    ).first()


    if user and user.check_password(password):
        return user


    return None
