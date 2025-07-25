from abc import ABC, abstractmethod
from app.domain.entities.student import Student
from sqlalchemy.future import select
from typing import Optional

async def get_all_students(session):
    result = await session.execute(select(Student))
    return result.scalars().all()

async def get_student_by_id(session, student_id: int):
    result = await session.execute(select(Student).where(Student.id == student_id))
    return result.scalar_one_or_none()

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
