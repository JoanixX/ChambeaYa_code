from abc import ABC, abstractmethod
from app.domain.entities.filter_match import FilterMatch
from app.domain.entities.student import Student
from app.domain.entities.job_offer import JobOffer
from typing import List, Dict

class CreateMatchPort(ABC):
    @abstractmethod
    async def match_job_student(self, estudiante: Student, filterMatch: FilterMatch):
        pass

    @abstractmethod
    async def match_student_job(self, job_offer: JobOffer, students: List[Student]) -> List[Dict]:
        pass