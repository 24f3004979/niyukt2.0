from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    drive_id = Column(Integer, ForeignKey("event_drives.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(20), default="applied")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Establish connection back to target EventDrive parent 
    drive = relationship("EventDrive", back_populates="applications")

    __table_args__ = (
        CheckConstraint("status IN ('applied', 'rejected', 'verified')", name="valid_app_status"),
    )

