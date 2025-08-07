from datetime import datetime

class FilterMatch:
    def __init__(self, job_offer_id: int, student_id: int, 
                 status: str, stage: int, created_at: datetime,
                 updated_at: datetime):
        self.job_offer_id = job_offer_id
        self.student_id = student_id
        self.status = status
        self.stage = stage
        self.created_at = created_at
        self.updated_at = updated_at