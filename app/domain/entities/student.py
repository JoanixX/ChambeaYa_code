from sqlalchemy import Column, Integer, String, SmallInteger, Date, ForeignKey
from app.infraestructure.database.base import Base

class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    career = Column(String(100), nullable=False)
    academic_cycle = Column(SmallInteger, nullable=False)
    location = Column(String(100), nullable=False)
    main_motivation = Column(String(100), nullable=True)
    description = Column(String(200), nullable=True)
    weekly_availability = Column(SmallInteger, nullable=True)
    preferred_modality = Column(SmallInteger, nullable=True)
    experience_id = Column(SmallInteger, ForeignKey('experience_detail.id'), nullable=True)
    date_of_birth = Column(Date, nullable=True)