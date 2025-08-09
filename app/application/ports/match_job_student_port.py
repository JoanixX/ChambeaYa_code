from abc import ABC, abstractmethod
from app.domain.entities.match_job_student import MatchJobStudent
from app.domain.entities.student import Student
from app.domain.entities.job_offer import JobOffer
from typing import List, Dict, Any

class MatchJobStudentPort(ABC):
    @abstractmethod
    async def register_match_job_student(self, match_job_student: Dict[str, Any]) -> MatchJobStudent:
        pass

    @abstractmethod
    async def match_job_student(self, student: Student, job_offers: List[JobOffer]):
        pass

    @abstractmethod
    async def match_student_job(self, job_offer: JobOffer, students: List[Student]):
        pass