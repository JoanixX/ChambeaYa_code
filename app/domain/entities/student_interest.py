from sqlalchemy import Column, Integer, SmallInteger, ForeignKey
from app.infraestructure.database.base import Base

class StudentInterest(Base):
    __tablename__ = 'student_interest'
    student_id = Column(Integer, ForeignKey('student.id'), primary_key=True)
    interest_id = Column(SmallInteger, ForeignKey('interest.id'), primary_key=True)
