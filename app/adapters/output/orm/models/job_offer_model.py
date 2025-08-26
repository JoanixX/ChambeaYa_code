from sqlalchemy import Column, Integer, ForeignKey, Date 
from sqlalchemy import JSON, String, SmallInteger, DateTime
from app.infraestructure.database.base import Base 
from sqlalchemy.sql import func 

class JobOfferModel(Base):
    __tablename__ = 'job_offer'
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('company.id'), nullable=False)
    title = Column(String(60), nullable=False)
    description = Column(String(200), nullable=False)
    required_hours = Column(SmallInteger, nullable=False)
    approximated_salary = Column(Integer, nullable=False)
    duration = Column(SmallInteger, nullable=False)
    start_date = Column(Date, nullable=False)
    modality = Column(SmallInteger, nullable=False)
    embedding = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())
    deleted_at = Column(DateTime, nullable=True)