from app.domain.entities.skill import Skill
from app.domain.repositories.skill_repository import SkillRepository
from typing import Dict, Any, Optional

class SkillService:
    def __init__(self, skill_repo: SkillRepository):
        self.skill_repo = skill_repo

    async def register_skill(self, skill_data: Dict[str, Any]) -> int:
        skill = self.skill_entity(skill_data)

        saved_model = await self.skill_repo.save(skill)
        if saved_model:
            return saved_model.id
        else:
            raise ValueError("Error al guardar el skill")
        
    async def get_skill(self, skill_id: int) -> Optional[Skill]:
        return await self.skill_repo.find_by_id(skill_id)
    
    async def get_all_skills(self) -> list[Skill]:
        return await self.skill_repo.get_all()
    
    async def delete_skill(self, skill_id: int) -> bool:
        return await self.skill_repo.delete(skill_id)
    
    async def get_name_by_id(self, skill_id: int) -> Optional[str]:
        return await self.skill_repo.get_name_by_id(skill_id)

    def skill_entity(self, skill_data: Dict[str, Any]) -> Skill:
        return Skill(
            id=0,
            name=skill_data.get("name", None)
        )