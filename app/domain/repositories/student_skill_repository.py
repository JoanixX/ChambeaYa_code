from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.student_skill import StudentSkill

class StudentSkillRepository(ABC):
    @abstractmethod
    def get_by_student_id(self, student_id: int) -> List[StudentSkill]:
        pass

    @abstractmethod
    def exists(self, student_id: int, skill_id: int) -> bool:
        pass

    @abstractmethod
    def save(self, student_skill: StudentSkill) -> StudentSkill:
        pass

    @abstractmethod
    def delete(self, student_id: int, skill_id: int) -> None:
        pass