from datetime import date, datetime

class JobOffer:
    def __init__(self, id: int, company_id: int, 
                 title: str, description: str, 
                 required_hours: int, approximated_salary: int,
                 duration: int, start_date: date, area_id: int,
                 experience_id: int, modality: int,
                 embedding: dict, created_at: datetime,
                 updated_at: datetime, deleted_at: datetime = None):
        self.id = id
        self.company_id = company_id
        self.title = title
        self.description = description
        self.required_hours = required_hours
        self.approximated_salary = approximated_salary
        self.duration = duration
        self.start_date = start_date
        self.area_id = area_id
        self.experience_id = experience_id
        self.modality = modality
        self.embedding = embedding
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at