from abc import ABC, abstractmethod
from app.domain.entities.skill import Skill
from typing import Optional, Dict, Any, List

class SkillPort(ABC):
    @abstractmethod
    async def register_skill(self, skill_data: Dict[str, Any]) -> Skill:
        pass

    @abstractmethod
    async def get_skill(self, skill_id: int) -> Optional[Skill]:
        pass

    @abstractmethod
    async def get_all_skills(self) -> List[Skill]:
        pass

    @abstractmethod
    async def delete_skill(self, skill_id: int) -> bool:
        pass