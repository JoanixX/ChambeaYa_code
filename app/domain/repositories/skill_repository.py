from abc import ABC, abstractmethod
from app.domain.entities.skill import Skill
from typing import Optional

class SkillRepository(ABC):
    @abstractmethod
    async def save(self, skill: Skill):
        pass

    @abstractmethod
    async def find_by_id(self, skill_id: int) -> Optional[Skill]:
        pass

    @abstractmethod
    async def get_all(self) -> list[Skill]:
        pass
    
    @abstractmethod
    async def delete(self, skill_id: int):
        pass

    @abstractmethod
    async def get_name_by_id(self, skill_id: int) -> Optional[str]:
        pass