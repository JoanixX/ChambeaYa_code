from sqlalchemy import Column, SmallInteger, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.infraestructure.database.base import Base

class ExperienceDetailModel(Base):
    __tablename__ = 'experience_detail'
    id = Column(SmallInteger, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'), nullable=True)
    job_offer_id = Column(Integer, ForeignKey('job_offer.id'), nullable=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)
    duration_in_months = Column(SmallInteger, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())
    deleted_at = Column(DateTime, nullable=True)