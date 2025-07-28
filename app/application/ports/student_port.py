from abc import ABC, abstractmethod
from app.domain.entities.student import Student
from typing import Optional, Dict, Any

class StudentPort(ABC):
    @abstractmethod
    async def register_student(self, student_data: Dict[str, Any]) -> Student:
        pass

    @abstractmethod
    async def get_student(self, student_id: int) -> Optional[Student]:
        pass

    @abstractmethod
    async def get_all_students(self) -> list[Student]:
        pass

    @abstractmethod
    async def update_student(self, student_id: int, student_data: Dict[str, Any]) -> Optional[Student]:
        pass

    @abstractmethod
    async def delete_student(self, student_id: int) -> bool:
        pass

    @abstractmethod
    async def validate_student_data(self, student_data: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    async def check_email_exists(self, email: str) -> bool:
        pass
