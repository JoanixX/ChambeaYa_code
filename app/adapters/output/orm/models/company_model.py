from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.infraestructure.database.base import Base

class CompanyModel(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    industry = Column(String(50), nullable=False)
    company_culture = Column(String(100), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())
    deleted_at = Column(DateTime, nullable=True)