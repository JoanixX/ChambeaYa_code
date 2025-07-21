from sqlalchemy import Column, Integer, String
from app.infraestructure.database.base import Base

class CompanyAreaModel(Base):
    __tablename__ = 'area'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)