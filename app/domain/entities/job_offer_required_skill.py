from sqlalchemy import Column, Integer, SmallInteger, ForeignKey
from app.infraestructure.database.base import Base

class JobOfferRequiredSkill(Base):
    __tablename__ = 'job_offer_required_skill'
    job_offer_id = Column(Integer, ForeignKey('job_offer.id'), primary_key=True)
    skill_id = Column(SmallInteger, ForeignKey('skill.id'), primary_key=True)
