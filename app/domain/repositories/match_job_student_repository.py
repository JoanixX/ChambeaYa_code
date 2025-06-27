from abc import ABC, abstractmethod
from app.domain.entities.match_job_student import MatchJobStudent

class MatchJobStudentRepository(ABC):
    @abstractmethod
    async def save(self, match_js: MatchJobStudent):
        pass

    @abstractmethod
    async def match_job_student(self, estudiante_id: int,
        job_offer_id: int) -> MatchJobStudent:
        pass