from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.student_interest import StudentInterest

class StudentInterestRepository(ABC):
    @abstractmethod
    def get_by_student_id(self, student_id: int) -> List[StudentInterest]:
        pass

    @abstractmethod
    def exists(self, student_id: int, interest_id: int) -> bool:
        pass

    @abstractmethod
    def save(self, student_interest: StudentInterest) -> StudentInterest:
        pass

    @abstractmethod
    def delete(self, student_id: int, interest_id: int) -> None:
        pass