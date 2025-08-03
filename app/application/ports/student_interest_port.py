from abc import ABC, abstractmethod
from app.domain.entities.student_interest import StudentInterest
from typing import List

class StudentInterestPort(ABC):
    @abstractmethod
    async def get_student_interests(self, student_id: int) -> List[StudentInterest]:
        pass

    @abstractmethod
    async def add_student_interest(self, student_interest: StudentInterest) -> StudentInterest:
        pass

    @abstractmethod
    async def delete_student_interest(self, student_id: int, interest_id: int) -> bool:
        pass