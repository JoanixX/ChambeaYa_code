from sqlalchemy import Column, Integer, SmallInteger, ForeignKey, Numeric, String, DateTime
from app.infraestructure.database.base import Base

class FilterMatch(Base):
    __tablename__ = 'filter_match'
    student_id = Column(Integer, ForeignKey('student.id'), primary_key=True)
    job_offer_id = Column(Integer, ForeignKey('job_offer.id'), primary_key=True)
    model_score = Column(Numeric(5,2), nullable=True)
    status = Column(String(30), nullable=True)
    filtered_at = Column(DateTime, nullable=True)
    stage = Column(SmallInteger, primary_key=True)