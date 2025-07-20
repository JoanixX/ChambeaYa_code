import enum
from typing import Optional
from datetime import date

class AgreementStatus(enum.Enum):
    pending = 'pending'
    active = 'active'
    completed = 'completed'
    cancelled = 'cancelled'

class Agreement:
    def __init__(self, id: int, job_offer_id: int, student_id: int, status: AgreementStatus, start_date: Optional[date], end_date: Optional[date]):
        self.id = id
        self.job_offer_id = job_offer_id
        self.student_id = student_id
        self.status = status
        self.start_date = start_date
        self.end_date = end_date
