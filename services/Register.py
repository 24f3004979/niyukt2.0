'''
    Registration Unit
    
    Student
        - Name, Email, Password
        - Information 
            resume

    Company
        - Name, email, password
        - Information
            company discription
'''
from sqlalchemy.orm import Session
from models.user import User

def register(db: Session, data: dict) -> User:
    '''
    data = {
        'username' : "name",
        'role' : 'admin',
        'password': 'password',
        'email' : 'email',
        'information' : 'information'
        }

    '''
 print("User Registration Initiating")

    existing_user = db.query(User).filter(
        User.username == data.get('username')
    ).first()
    if existing_user:
        raise ValueError(f"Registration Failed | USER EXIST WITH GIVEN NAME")

    # Role and status verification

    target_role = data.get('role')
    if target_role == 'admin':
        raise ValueError(f"SECURITY DENIED ADMIN REGISTRATION NOT ALLOWED")
    final_status = 'freezed'
    if target_role == 'student':
        final_status = 'active'
    secured_password = hashpassword(data['password'])

    # Profile Information requries way to upload the document into the portal

    # Registration with User model
    new_user = User(
        username = data['username'],
        password=secured_password,
        role=target_role,
        account_status=final_status,
        profile_info=data.get('profile_info', {})
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
