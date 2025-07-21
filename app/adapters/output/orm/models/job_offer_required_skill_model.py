from sqlalchemy import Column, Integer, ForeignKey
from app.infraestructure.database.base import Base

class JobOfferRequiredSkillModel(Base):
    __tablename__ = 'job_offer_required_skill'
    job_offer_id = Column(Integer, ForeignKey('job_offer.id'), nullable=False)
    skill_id = Column(Integer, ForeignKey('skill.id'), nullable=False)