from sqlalchemy import Column, Integer, SmallInteger, ForeignKey
from app.infraestructure.database.base import Base

class StudentSkill(Base):
    __tablename__ = 'student_skill'
    student_id = Column(Integer, ForeignKey('student.id'), primary_key=True)
    skill_id = Column(SmallInteger, ForeignKey('skill.id'), primary_key=True)
