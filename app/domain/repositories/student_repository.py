from abc import ABC, abstractmethod
from app.domain.entities.student import Student
from sqlalchemy.future import select
from typing import Optional

async def get_all_students(session):
    result = await session.execute(select(Student))
    return result.scalars().all()

class StudentRepository(ABC):
    @abstractmethod
    async def save(self, student: Student):
        pass

    @abstractmethod
    async def find_by_id(self, student_id: int) -> Optional[Student]:
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[Student]:
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
