from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey
from database import Base

class DocElement(Base):
    __tablename__ = "doc_elements"

    # SQLite manages this assignment completely. No need to pass it in init.
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    compressed_blob = Column(LargeBinary, nullable=True)

