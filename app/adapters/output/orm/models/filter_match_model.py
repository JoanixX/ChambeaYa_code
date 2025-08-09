from sqlalchemy.sql import func
from app.infraestructure.database.base import Base

from sqlalchemy import Column, Integer, SmallInteger, ForeignKey, String, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from app.infraestructure.database.base import Base

class FilterMatchModel(Base):
    __tablename__ = 'filter_match'
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_offer_id = Column(Integer, ForeignKey('job_offer.id'), nullable=True)
    student_id = Column(Integer, ForeignKey('student.id'), nullable=True)
    status = Column(String(30), nullable=False)
    stage = Column(SmallInteger, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())
    __table_args__ = (
        UniqueConstraint('student_id', 'job_offer_id', name='uq_student_job_offer'),
    )