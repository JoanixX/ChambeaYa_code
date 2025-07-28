from abc import ABC, abstractmethod
from app.domain.entities.skill import Skill

class SkillPort(ABC):
    @abstractmethod
    async def add_skill(self, skill: Skill) -> Skill:
        pass

    @abstractmethod
    async def validate_skill_data(self, skill_data: dict) -> bool:
        pass

    @abstractmethod
    async def check_skill_exists(self, skill_name: str) -> bool:
        pass