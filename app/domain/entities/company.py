from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    tax_id = Column(String(20), nullable=False)
    industry = Column(String, nullable=False)
    challenge_area_id = Column(Integer, nullable=False)
    challenge_description = Column(String, nullable=True)
    company_culture = Column(String, nullable=False)
    required_hours = Column(Integer, nullable=False)
    project_modality_id = Column(Integer, nullable=False)
    contact_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
