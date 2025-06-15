from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    date_of_birth = Column(Date, nullable=False)
    experience_id = Column(Integer, nullable=False)
    enrollment_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    location = Column(String, nullable=False)
    star_skill_id = Column(Integer, nullable=False)
    main_motivation_id = Column(Integer, nullable=False)
    weekly_availability = Column(Integer, nullable=False)
    preferred_modality_id = Column(Integer, nullable=False)
    career = Column(String, nullable=False)
    academic_cycle = Column(Integer, nullable=False)