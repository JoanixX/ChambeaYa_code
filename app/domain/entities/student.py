from datetime import date, datetime

class Student:
    def __init__(self, id: int, career: str, academic_cycle: int, weekly_availability: int,
                 preferred_modality: int, embedding: dict = None, created_at: datetime = None,
                 updated_at: datetime = None, deleted_at: datetime = None):
        self.id = id
        self.career = career
        self.academic_cycle = academic_cycle
        self.weekly_availability = weekly_availability
        self.preferred_modality = preferred_modality
        self.embedding = embedding
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at