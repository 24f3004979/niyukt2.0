from app.models.user import User
from app.extensions import db



def get_all_users():

    return User.query.all()



def create_user(data):
    '''
    Format for information
    data {
        email, username, password, role, account_status
    }
    '''
    user = User(
        email=data["email"],
        username=data["username"],
        password=data["password"],
        role=data.get(
            "role",
            "student"
        ),
        account_status=data.get(
            "account_status",
            "active"
        )
    )


    db.session.add(user)
    db.session.commit()


    return user
