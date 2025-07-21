from sqlalchemy import Column, SmallInteger, String
from app.infraestructure.database.base import Base

class ExperienceDetailModel(Base):
    __tablename__ = 'experience_detail'
    id = Column(SmallInteger, primary_key=True)
    name = Column(String(50))
    description = Column(String(255))
    duration_in_months = Column(SmallInteger)