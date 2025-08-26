from sqlalchemy import Column, Integer, ForeignKey, SmallInteger
from app.infraestructure.database.base import Base

class CompanyAreaModel(Base):
    __tablename__ = 'company_area'
    company_id = Column(Integer, ForeignKey('company.id'), primary_key=True)
    area_id = Column(SmallInteger, ForeignKey('area.id'), primary_key=True)