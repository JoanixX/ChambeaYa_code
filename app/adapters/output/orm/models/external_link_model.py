from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.infraestructure.database.base import Base

class ExternalLinkModel(Base):
    __tablename__ = 'external_link'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'), nullable=False)
    link = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())