from app.models.user import User
from app.extensions import db



def register_user(data):

    ''' Try Except block required to handle the Existing user account information fallback '''
    
    print(f"Information Recieved for the registration : {data}")
    
    st="active"
    if data.get("role") == 'company':
        st='blocked'

    user = User(
        email=data["email"],
        username=data["username"],
        role=data.get(
            "role",
            "student"
        ),
        account_status=st
    )


    user.set_password(
        data["password"]
    )


    db.session.add(user)
    db.session.commit()


    return user



def authenticate(username,password):
    ''' Authentication Dummy function for basic working '''
    user = User.query.filter_by(
        username=username
    ).first()

    print(f"User found with given informaiton {user}")

    # Making user check
    if user and user.check_password_hash(password):
        print('Checking password hash')
        return user


    return None
