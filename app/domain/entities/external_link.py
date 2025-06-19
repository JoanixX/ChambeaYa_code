from sqlalchemy import Column, Integer, String, ForeignKey
from app.infraestructure.database.base import Base

class ExternalLink(Base):
    __tablename__ = 'external_link'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'), nullable=False)
    link = Column(String(255), nullable=False)
