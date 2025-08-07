from sqlalchemy import Column, Integer, String, SmallInteger
from sqlalchemy import DateTime, Date, ForeignKey, JSON
from sqlalchemy.sql import func
from app.infraestructure.database.base import Base

class StudentModel(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    career = Column(String(100), nullable=False)
    academic_cycle = Column(SmallInteger, nullable=False)
    location = Column(String(100), nullable=False)
    main_motivation = Column(String(100), nullable=False)
    description = Column(String(200), nullable=False)
    weekly_availability = Column(SmallInteger, nullable=False)
    preferred_modality = Column(SmallInteger, nullable=False)
    experience_id = Column(SmallInteger, ForeignKey('experience_detail.id'), nullable=True)
    date_of_birth = Column(Date, nullable=False)
    embedding = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())
    deleted_at = Column(DateTime, nullable=True)