from typing import Dict, Any, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.output.orm.repositories.skill_repository_impl import SkillRepositoryImpl
from app.application.ports.skill_port import SkillPort
from app.domain.entities.skill import Skill

class SkillPortImpl(SkillPort):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.skill_repo = SkillRepositoryImpl(session)

    async def register_skill(self, skill_data: Dict[str, Any]) -> Skill:
        skill = Skill(
            id=0,
            name=skill_data["name"]
        )

        saved_skill = await self.skill_repo.save(skill)
        return saved_skill
    
    async def get_skill(self, skill_id: int) -> Optional[Skill]:
        return await self.skill_repo.find_by_id(skill_id)
    
    async def get_all_skills(self) -> List[Skill]:
        return await self.skill_repo.get_all()
    
    async def delete_skill(self, skill_id: int) -> bool:
        return await self.skill_repo.delete(skill_id)
    
    async def get_skill_name_by_id(self, skill_id: int) -> Optional[str]:
        return await self.skill_repo.get_name_by_id(skill_id)