from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, JSON
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), default="student")
    account_status = Column(String(20), default="freezed")
    profile_info = Column(JSON, default=dict)
    asset_id = Column(Integer, ForeignKey("doc_elements.id", ondelete="SET NULL"), nullable=True)

    __table_args__ = (
        CheckConstraint("role IN ('admin', 'student', 'company')", name="valid_user_role"),
        CheckConstraint("account_status IN ('active', 'freezed')", name="valid_account_status"),
    )

