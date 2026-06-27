from datetime import datetime, timedelta
from database import SessionLocal
from models.user import User
from models.drive import EventDrive
from models.application import Application
from models.doc import DocElement
from services.auth import hash_password

def run_comprehensive_model_test():
    print("=" * 60)
    print("STARTING COMPREHENSIVE DATABASE MODEL & TRIGGER TEST")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # 1. TEST EVENTDRIVE MODEL (Active Drive)
        print("\n[1/5] Testing EventDrive Model (Active)...")
        active_drive = EventDrive(
            title="Google Summer Internship 2026",
            info_doc="https://google.com",
            meta_data={"allowed_degrees": ["B.Tech", "MCA"], "min_gpa": 3.5},
            deadline_stamp=datetime.utcnow() + timedelta(days=5) # Deadline is 5 days in the future
        )
        db.add(active_drive)
        db.commit()
        db.refresh(active_drive)
        print(f"-> SUCCESS: Active Drive Created. SQLite ID: {active_drive.id}")

        # 2. TEST USER MODEL
        print("\n[2/5] Testing User Model...")
        student_user = User(
            username="alex_jones",
            password=hash_password("student_pass_123"),
            role="student",
            account_status="active",
            profile_info={"major": "Computer Science", "gpa": 3.8}
        )
        db.add(student_user)
        db.commit()
        db.refresh(student_user)
        print(f"-> SUCCESS: Student User Created. SQLite ID: {student_user.id}")

        # 3. TEST DOCELEMENT MODEL (Linking back to User)
        print("\n[3/5] Testing DocElement Model & Profile Linking...")
        resume_doc = DocElement(
            user_id=student_user.id,
            compressed_blob=b"%PDF-1.5 simulated resume raw binary content"
        )
        db.add(resume_doc)
        db.commit()
        db.refresh(resume_doc)
        print(f"-> SUCCESS: DocElement Created. SQLite ID: {resume_doc.id}")
        
        # Link this newly generated asset ID right back onto our User account profile column
        student_user.asset_id = resume_doc.id
        db.commit()
        print(f"-> SUCCESS: Connected Asset ID {resume_doc.id} onto User ID {student_user.id}")

        # 4. TEST APPLICATION MODEL (On-Time / Valid Case)
        print("\n[4/5] Testing Valid On-Time Application...")
        valid_app = Application(
            student_id=student_user.id,
            drive_id=active_drive.id,
            status="applied",
            created_at=datetime.utcnow() # Current time is BEFORE the 5-day deadline
        )
        db.add(valid_app)
        db.commit()
        db.refresh(valid_app)
        print(f"-> SUCCESS: On-Time Application Created. SQLite ID: {valid_app.id}")

        # 5. TEST SQLITE TRIGGER & EXPIRED EVENTDRIVE (Invalid Case)
        print("\n[5/5] Testing SQLite Deadline Enforcement Trigger...")
        
        # Create an expired drive where the deadline passed yesterday
        expired_drive = EventDrive(
            title="Expired Legacy Placement Drive",
            info_doc="https://example.com",
            meta_data={"archive": True},
            deadline_stamp=datetime.utcnow() - timedelta(days=1) # Expired 1 day ago
        )
        db.add(expired_drive)
        db.commit()
        db.refresh(expired_drive)
        print(f"   -> Setup: Expired Drive created with ID: {expired_drive.id}")

        # Attempt to insert an application into the expired drive
        late_app = Application(
            student_id=student_user.id,
            drive_id=expired_drive.id,
            status="applied",
            created_at=datetime.utcnow() # Current time is AFTER the drive's deadline stamp
        )
        db.add(late_app)
        
        print("   -> Attempting to commit late application to DB (Should fail)...")
        db.commit() # This line should trigger the SQLite ABORT statement!
        
        # If execution reaches here, something went wrong with the trigger setup
        print("❌ FAILURE: The database allowed a late application to be written!")

    except Exception as db_error:
        db.rollback()
        # Look specifically for our trigger's custom message inside the exception string
        error_msg = str(db_error)
        if "Application Rejected" in error_msg:
            print("\n" + "=" * 60)
            print("🎉 ALL TESTS PASSED SUCCESSFULLY! 🎉")
            print("=" * 60)
            print(f"The SQLite trigger caught the late submission perfectly.\nDatabase Error Blocked: {error_msg}")
        else:
            print(f"❌ CRITICAL FAILURE: Test crashed due to unexpected error: {db_error}")
            
    finally:
        db.close()

if __name__ == "__main__":
    run_comprehensive_model_test()

