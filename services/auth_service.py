import bcrypt
from sqlalchemy.orm import Session
from models.user import User

def hash_password(password: str) -> str:
    """Converts plain-text passwords into secure, unreadable cryptographic hashes."""
    salt = bcrypt.gensalt()
    # Returns the hash string decoded as a standard string for database storage
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compares an incoming login password against the database hash string."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def register_user(db: Session, data: dict) -> User:
    """
    Validates availability and registers a new User account.
    Expected dict structure: {'username', 'password', 'role', 'profile_info'}
    """
    print(f"data Recieved for registration : {data}")
    # 1. Prevent duplicate account registrations
    existing_user = db.query(User).filter(User.username == data['username']).first()
    if existing_user:
        raise ValueError(f"Registration Failed: Username '{data['username']}' is taken.")
    
    # 2. Prevent arbitrary admin accounts through user registration loops
    target_role = data.get('role')
    if target_role == 'admin':
        raise ValueError("Security Denied: Cannot register administrative rights via public portals.")
    
    final_status = 'freezed'
    # If target role is student then its activated by default or company would need approval
    if target_role == 'student':
        final_status = 'active'

    # 3. Securely hash the password string
    secured_password = hash_password(data['password'])

    # 4. Initialize model object and let SQLite handle the ID generation
    new_user = User(
        username=data['username'],
        password=secured_password,
        role=target_role,
        account_status=final_status,
        profile_info=data.get('profile_info', {})
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user) # Automatically pulls down the auto-incremented SQLite ID
    return new_user

def authenticate_user(db: Session, username: str, plain_password: str) -> User:
    """
    Validates application user credentials.
    Returns the User model if valid; raises an exception for any failures.
    """
    user = db.query(User).filter(User.username == username).first()
    
    # 1. Check if the user exists
    if not user:
        raise ValueError("Login Failed: Invalid username | Does not Exist")
    
    # 2. Check if the account has been frozen
    if user.account_status == "freezed":
        raise PermissionError("Access Denied: This account has been frozen by administration.")

    # 3. Check if the password matches the hash
    if not verify_password(plain_password, user.password):
        raise ValueError("Login Failed: Invalid Password")

    return user

