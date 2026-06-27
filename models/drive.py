from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship
from database import Base

class EventDrive(Base):
    __tablename__ = "event_drives"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    info_doc = Column(String(1000))
    meta_data = Column(JSON, default=dict)
    deadline_stamp = Column(DateTime, nullable=False)

    # Configures target child relationships links
    applications = relationship("Application", back_populates="drive", cascade="all, delete-orphan")

