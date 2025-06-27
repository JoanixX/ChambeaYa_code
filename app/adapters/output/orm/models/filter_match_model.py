from sqlalchemy import Column, Integer, SmallInteger, ForeignKey, String
from app.infraestructure.database.base import Base

class FilterMatchModel(Base):
    __tablename__ = 'filter_match'
    job_offer_id = Column(Integer, ForeignKey('job_offer.id'), primary_key=True)
    status = Column(String(30), nullable=False)
    stage = Column(SmallInteger, primary_key=True)
