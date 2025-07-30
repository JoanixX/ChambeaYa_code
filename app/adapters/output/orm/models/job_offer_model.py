from sqlalchemy import Column, Integer, ForeignKey, Date, JSON, VARCHAR, SMALLINT
from app.infraestructure.database.base import Base  

class JobOfferModel(Base):
    __tablename__ = 'job_offer'
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('company.id'), nullable=False)
    title = Column(VARCHAR(60), nullable=False)
    description = Column(VARCHAR(200), nullable=False)
    required_hours = Column(Integer, nullable=False)
    approximated_salary = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    area_id = Column(Integer, ForeignKey('area.id'), nullable=False)
    experience_id = Column(Integer, ForeignKey('experience_detail.id'), nullable=False)
    modality = Column(SMALLINT, nullable=False)
    embedding = Column(JSON, nullable=True)