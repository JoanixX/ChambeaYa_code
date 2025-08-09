from sqlalchemy import Column, SmallInteger, String
from app.infraestructure.database.base import Base

class InterestModel(Base):
    __tablename__ = 'interest'
    id = Column(SmallInteger, primary_key=True)
    name = Column(String(50), nullable=False)