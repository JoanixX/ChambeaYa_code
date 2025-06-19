from sqlalchemy import Column, SmallInteger, String
from app.infraestructure.database.base import Base

class ExperienceDetail(Base):
    __tablename__ = 'experience_detail'
    id = Column(SmallInteger, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    duration_in_months = Column(SmallInteger, nullable=True)
