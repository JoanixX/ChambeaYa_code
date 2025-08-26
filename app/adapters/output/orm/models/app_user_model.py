import enum
from sqlalchemy import Column, Integer, String, Enum, DateTime, Date
from sqlalchemy.sql import func
from app.infraestructure.database.base import Base

class UserRole(enum.Enum):
    admin = 'admin'
    company = 'company'
    student = 'student'

class AppUserModel(Base):
    __tablename__ = 'app_user'
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    dni = Column(String(8), nullable=False)
    cv_url = Column(String(512), nullable=True)
    name = Column(String(50), nullable=True)
    location = Column(String(100), nullable=True)
    ruc = Column(String(50), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    main_motivation = Column(String(200), nullable=True)
    description = Column(String(350), nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole, name="user_role"), nullable=False)
    related_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())
    deleted_at = Column(DateTime, nullable=True)