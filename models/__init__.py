# Import every class so Base knows they exist before building tables
from database import Base
from models.doc import DocElement
from models.user import User
from models.drive import EventDrive
from models.application import Application

# Package exposition variable list
__all__ = ["Base", "DocElement", "User", "EventDrive", "Application"]

