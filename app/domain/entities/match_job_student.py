from sqlalchemy import Column, Integer, SmallInteger, ForeignKey, Numeric, String, DateTime
from app.infraestructure.database.base import Base

class MatchJobStudent(Base):
    __tablename__ = 'match_job_student'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'), nullable=False)
    job_offer_id = Column(Integer, ForeignKey('job_offer.id'), nullable=False)
    score = Column(Numeric(5,2), nullable=False)
    match_date = Column(DateTime, nullable=False)
    rank = Column(SmallInteger, nullable=False)
