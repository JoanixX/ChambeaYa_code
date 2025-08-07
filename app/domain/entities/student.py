from datetime import date, datetime
from typing import Optional

class Student:
    def __init__(self, id: int, name: str, email: str, 
                 career: str, academic_cycle: int, 
                 location: str, main_motivation: str, 
                 description: str, weekly_availability: int, 
                 preferred_modality: int, experience_id: int, 
                 date_of_birth: date, embedding: dict, 
                 created_at: datetime, updated_at: datetime, 
                 deleted_at: datetime = None):
        self.id = id
        self.name = name
        self.email = email
        self.career = career
        self.academic_cycle = academic_cycle
        self.location = location
        self.main_motivation = main_motivation
        self.description = description
        self.weekly_availability = weekly_availability
        self.preferred_modality = preferred_modality
        self.experience_id = experience_id
        self.date_of_birth = date_of_birth
        self.embedding = embedding
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at