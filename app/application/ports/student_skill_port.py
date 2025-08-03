from abc import ABC, abstractmethod
from app.domain.entities.student_skill import StudentSkill
from typing import List

class StudentSkillPort(ABC):
    @abstractmethod
    async def get_student_skills(self, student_id: int) -> List[StudentSkill]:
        pass

    @abstractmethod
    async def add_student_skill(self, student_skill: StudentSkill) -> StudentSkill:
        pass

    @abstractmethod
    async def delete_student_skill(self, student_id: int, skill_id: int) -> bool:
        pass