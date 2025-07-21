from sqlalchemy import Column, Integer, VARCHAR
from app.infraestructure.database.base import Base

class AreaModel(Base):
    __tablename__ = 'area'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(50), nullable=False)