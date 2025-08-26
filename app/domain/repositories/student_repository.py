from abc import ABC, abstractmethod
from app.domain.entities.student import Student
from sqlalchemy.future import select
from typing import Optional

class StudentRepository(ABC):
    @abstractmethod
    async def get_enriched_students(self, session) -> list:
        pass
    
    @abstractmethod
    async def save(self, student: Student):
        pass

    @abstractmethod
    async def find_by_id(self, student_id: int) -> Optional[Student]:
        pass

    @abstractmethod
    async def get_all(self) -> list[Student]:
        pass

    @abstractmethod
    async def update(self, student: Student):
        pass

    @abstractmethod
    async def delete(self, student_id: int):
        pass
