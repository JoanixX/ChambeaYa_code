from sqlalchemy.future import select
from sqlalchemy import delete
from typing import Optional
from app.adapters.output.orm.models.skill_model import SkillModel
from app.domain.entities.skill import Skill
from app.domain.repositories.skill_repository import SkillRepository

class SkillRepositoryImpl(SkillRepository):
    def __init__(self, session):
        self.session = session
    
    async def save(self, skill: Skill):
        model = SkillModel(
            name=skill.name
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def find_by_id(self, skill_id: int) -> Optional[Skill]:
        result = await self.session.execute(select(SkillModel).where(SkillModel.id == skill_id))
        model = result.scalar_one_or_none()
        if model:
            return Skill(
                id=model.id,
                name=model.name
            )
        return None

    async def get_all(self) -> list[Skill]:
        result = await self.session.execute(select(SkillModel))
        models = result.scalars().all()
        skills = []
        for model in models:
            skills.append(
                Skill(
                id=model.id,
                name=model.name
            )
        )
        return skills

    async def delete(self, skill_id: int) -> bool:
        result = await self.session.execute(select(SkillModel).where(SkillModel.id == skill_id))
        model = result.scalar_one_or_none()
        if not model:
            return False

        await self.session.execute(delete(SkillModel).where(SkillModel.id == skill_id))
        await self.session.commit()
        return True

    async def get_name_by_id(self, skill_id: int) -> Optional[str]:
        result = await self.session.execute(select(SkillModel.name).where(SkillModel.id == skill_id))
        name = result.scalar_one_or_none()
        return name if name else None