import enum
from datetime import date, datetime

class AgreementStatus(enum.Enum):
    pending = 'pending'
    active = 'active'
    completed = 'completed'
    cancelled = 'cancelled'

class Agreement:
    def __init__(self, id: int, job_offer_id: int, student_id: int, status: AgreementStatus,
                 start_date: date = None, end_date: date = None, created_at: datetime = None,
                 updated_at: datetime = None, deleted_at: datetime = None):
        self.id = id
        self.job_offer_id = job_offer_id
        self.student_id = student_id
        self.status = status
        self.start_date = start_date
        self.end_date = end_date
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at