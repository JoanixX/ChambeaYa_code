from sqlalchemy import Column, Integer, ForeignKey
from app.infraestructure.database.base import Base
from sqlalchemy.dialects.mysql import SMALLINT

class StudentSkillModel(Base):
    __tablename__ = 'student_skill'
    student_id = Column(Integer, ForeignKey('student.id'), primary_key=True)
    skill_id = Column(SMALLINT, ForeignKey('skill.id'), primary_key=True)