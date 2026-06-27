import sys
from database import SessionLocal
from models.user import User
from services.auth import hash_password

def seed_admin():
    print("Initiating Administrative seeding checks...")
    db = SessionLocal()
    try:
        # Check if an administrator account already exists
        admin_exists = db.query(User).filter(User.role == "admin").first()
        if admin_exists:
            print(f"Aborted: Admin account already exists (ID: {admin_exists.id}).")
            return

        # Configure secure credentials
        admin_username = "admin"
        admin_password = "1234" # Change this for production!

        new_admin = User(
            username=admin_username,
            password=hash_password(admin_password),
            role="admin",
            account_status="active",
            profile_info={"title": "Root System Admin", "clearance": "level_5"}
        )

        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)

        print("-" * 50)
        print("ADMIN ACCOUNT INSTANTIATED SUCCESSFULLY")
        print(f"Generated Database ID : {new_admin.id}")
        print(f"Username              : {new_admin.username}")
        print("-" * 50)

    except Exception as e:
        db.rollback()
        print(f"Seeding operation crashed: {e}", file=sys.stderr)
    finally:
        db.close()

if __name__ == "__main__":
    seed_admin()

