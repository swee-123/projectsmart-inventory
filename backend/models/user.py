from sqlalchemy import Column, Integer, String, Enum
from backend.database import Base
import enum


class UserRole(str, enum.Enum):
    admin = "Admin"
    manager = "Manager"
    staff = "Staff"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.staff)
