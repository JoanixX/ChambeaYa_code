from datetime import datetime

class ExperienceDetail:
    def __init__(self, id: int, student_id: int, job_offer_id: int, 
                 name: str, description: str, duration_in_months: int, 
                 created_at: datetime = None, updated_at: datetime = None, 
                 deleted_at: datetime = None):
        self.id = id
        self.student_id = student_id
        self.job_offer_id = job_offer_id
        self.name = name
        self.description = description
        self.duration_in_months = duration_in_months
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at