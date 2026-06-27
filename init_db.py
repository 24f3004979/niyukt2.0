from sqlalchemy import DDL, event
from database import engine, Base
# Importing package imports all underlying sub-models cleanly 
import models 

sqlite_deadline_trigger = """
CREATE TRIGGER trigger_enforce_deadline
BEFORE INSERT ON applications
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'Application Rejected: The deadline for this drive has already passed.')
    WHERE NEW.created_at > (SELECT deadline_stamp FROM event_drives WHERE id = NEW.drive_id);
END;
"""

# Attach trigger to the structural application class module block definition
event.listen(models.Application.__table__, "after_create", DDL(sqlite_deadline_trigger))

def init_database():
    print("Generating SQLite scheme layout...")
    Base.metadata.create_all(bind=engine)
    print("Database built successfully.")

if __name__ == "__main__":
    init_database()

