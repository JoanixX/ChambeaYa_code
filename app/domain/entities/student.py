from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    enrollment_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    #experience_id = Column(Integer, ForeignKey('experience.id'), nullable=True)