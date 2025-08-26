from sqlalchemy import Column, Integer, String, SmallInteger
from sqlalchemy import DateTime, Date, ForeignKey, JSON
from sqlalchemy.sql import func
from app.infraestructure.database.base import Base

class StudentModel(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    career = Column(String(100), nullable=False)
    academic_cycle = Column(SmallInteger, nullable=False)
    weekly_availability = Column(SmallInteger, nullable=False)
    preferred_modality = Column(SmallInteger, nullable=False)
    embedding = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())
    deleted_at = Column(DateTime, nullable=True)