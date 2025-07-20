from abc import ABC, abstractmethod
from app.domain.entities.student import Student

class RegisterStudentPort(ABC):
    @abstractmethod
    async def register_student(self, student: Student) -> Student:
        pass

    @abstractmethod
    async def validate_student_data(self, student_data: dict) -> bool:
        pass

    @abstractmethod
    async def check_email_exists(self, email: str) -> bool:
        pass
