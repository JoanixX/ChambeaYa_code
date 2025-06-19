from sqlalchemy import Column, Integer, SmallInteger, ForeignKey, Enum, Date
import enum
from app.infraestructure.database.base import Base

class AgreementStatus(enum.Enum):
    pending = 'pending'
    active = 'active'
    completed = 'completed'
    cancelled = 'cancelled'

class Agreement(Base):
    __tablename__ = 'agreement'
    id = Column(Integer, primary_key=True)
    job_offer_id = Column(Integer, ForeignKey('job_offer.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('student.id'), nullable=False)
    status = Column(Enum(AgreementStatus), nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
