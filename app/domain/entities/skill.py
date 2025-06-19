from sqlalchemy import Column, SmallInteger, String
from app.infraestructure.database.base import Base

class Skill(Base):
    __tablename__ = 'skill'
    id = Column(SmallInteger, primary_key=True)
    name = Column(String(50), nullable=False)
