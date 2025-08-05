from abc import ABC, abstractmethod
from app.domain.entities.filter_match import FilterMatch
from app.domain.entities.student import Student
from app.domain.entities.job_offer import JobOffer
from typing import List, Dict

class MatchJobStudentPort(ABC):
    @abstractmethod
    async def match_job_student(self, student: Student, job_offers: List[JobOffer]):
        pass

    @abstractmethod
    async def match_student_job(self, job_offer: JobOffer, students: List[Student]):
        pass