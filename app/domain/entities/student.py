from datetime import date
from typing import Optional

class Student:
    def __init__(self, id: int, name: str, email: str, career: str, academic_cycle: int, location: str, main_motivation: str, description: str, weekly_availability: int, preferred_modality: int, experience_id: Optional[int], date_of_birth: date, embedding: dict):
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