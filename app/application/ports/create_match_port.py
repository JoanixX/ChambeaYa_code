from abc import ABC, abstractmethod
from app.domain.entities.filter_match import FilterMatch
from app.domain.entities.student import Student

class CreateMatchPort(ABC):
    @abstractmethod
    async def match_job_student(self, estudiante: Student, filterMatch: FilterMatch):
        pass