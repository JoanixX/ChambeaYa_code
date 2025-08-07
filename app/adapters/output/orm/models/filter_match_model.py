from sqlalchemy import Column, Integer, SmallInteger, ForeignKey, String, DateTime
from sqlalchemy.sql import func
from app.infraestructure.database.base import Base

class FilterMatchModel(Base):
    __tablename__ = 'filter_match'
    job_offer_id = Column(Integer, ForeignKey('job_offer.id'), primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'), primary_key=True)
    status = Column(String(30), primary_key=True, nullable=False)
    stage = Column(SmallInteger, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())