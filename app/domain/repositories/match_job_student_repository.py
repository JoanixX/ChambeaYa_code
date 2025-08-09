from abc import ABC, abstractmethod
from app.domain.entities.match_job_student import MatchJobStudent
from app.domain.entities.student import Student
from app.domain.entities.job_offer import JobOffer
from typing import List

class MatchJobStudentRepository(ABC):
    @abstractmethod
    async def save(self, match_js: MatchJobStudent):
        pass

    @abstractmethod
    async def match_best_from_student(self, student: Student, job_offers: List[JobOffer]) -> MatchJobStudent:
        pass

    @abstractmethod
    async def match_best_from_job_offer(self, job_offer: JobOffer, students: List[Student]) -> MatchJobStudent:
        pass