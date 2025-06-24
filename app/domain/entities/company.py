from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey
from app.infraestructure.database.base import Base

class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True)
    RUC = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    industry = Column(String(50), nullable=False)
    area_id = Column(SmallInteger, ForeignKey('area.id'), nullable=False)
    contact_name = Column(String(100), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    company_culture = Column(String(100), nullable=False)
