from sqlalchemy import Column, Integer, String, Enum
import enum
from app.infraestructure.database.base import Base

class UserRole(enum.Enum):
    admin = 'admin'
    company = 'company'
    student = 'student'

class AppUser(Base):
    __tablename__ = 'app_user'
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole, name="user_role"), nullable=False)
    related_id = Column(Integer, nullable=False)
