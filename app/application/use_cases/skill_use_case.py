from app.domain.entities.skill import Skill
from app.domain.repositories.skill_repository import SkillRepository
from typing import Optional, List

class SkillUseCase:
    def __init__(self, skill_repository: SkillRepository):
        self.skill_repository = skill_repository

    async def get_by_id(self, skill_id: int) -> Optional[Skill]:
        return await self.skill_repository.find_by_id(skill_id)

    async def get_all(self) -> List[Skill]:
        return await self.skill_repository.get_all()

    async def create(self, skill: Skill) -> Optional[Skill]:
        return await self.skill_repository.save(skill)

    async def update(self, skill: Skill) -> Optional[Skill]:
        return await self.skill_repository.update(skill)

    async def delete(self, skill_id: int):
        await self.skill_repository.delete(skill_id)