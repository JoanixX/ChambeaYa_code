from sqlalchemy import Column, Integer, ForeignKey, SmallInteger
from app.infraestructure.database.base import Base

class JobOfferAreaModel(Base):
    __tablename__ = 'job_offer_area'
    job_offer__id = Column(Integer, ForeignKey('job_offer.id'), primary_key=True)
    area_id = Column(SmallInteger, ForeignKey('area.id'), primary_key=True)