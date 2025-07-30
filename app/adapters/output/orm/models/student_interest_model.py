from sqlalchemy import Column, Integer, ForeignKey
from app.infraestructure.database.base import Base
from sqlalchemy.dialects.postgresql import SMALLINT

class StudentInterestModel(Base):
    __tablename__ = 'student_interest'
    student_id = Column(Integer, ForeignKey('student.id'), primary_key=True)
    interest_id = Column(SMALLINT, ForeignKey('interest.id'), primary_key=True)