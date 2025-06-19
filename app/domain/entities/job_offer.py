from sqlalchemy import Column, Integer, SmallInteger, String, Date, ForeignKey
from app.infraestructure.database.base import Base

class JobOffer(Base):
    __tablename__ = 'job_offer'
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('company.id'), nullable=False)
    title = Column(String(60), nullable=False)
    description = Column(String(200), nullable=False)
    required_hours = Column(SmallInteger, nullable=False)
    approximated_salary = Column(Integer, nullable=True)
    duration = Column(SmallInteger, nullable=True)
    start_date = Column(Date, nullable=True)
    area_id = Column(SmallInteger, ForeignKey('area.id'), nullable=False)
    experience_id = Column(SmallInteger, ForeignKey('experience_detail.id'), nullable=True)
    modality = Column(SmallInteger, nullable=True)
