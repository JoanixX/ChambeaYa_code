from abc import ABC, abstractmethod
from app.domain.entities.student import Student
from typing import Optional, Dict, Any, List

class StudentPort(ABC):
    @abstractmethod
    async def get_enriched_students(self) -> List[Student]:
        pass
    
    @abstractmethod
    async def register_student(self, student_data: Dict[str, Any]) -> Student:
        pass

    @abstractmethod
    async def get_student(self, student_id: int) -> Optional[Student]:
        pass

    @abstractmethod
    async def get_all_students(self) -> List[Student]:
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