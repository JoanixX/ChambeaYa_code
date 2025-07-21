from sqlalchemy import Column, Integer, ForeignKey
from app.infraestructure.database.base import Base

class StudentInterestModel(Base):
    __tablename__ = 'student_interest'
    student_id = Column(Integer, ForeignKey('student.id'), nullable=False)
    interest_id = Column(Integer, ForeignKey('interest.id'), nullable=False)