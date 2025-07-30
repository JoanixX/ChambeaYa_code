from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
from app.adapters.output.orm.models.skill_model import SkillModel
from app.domain.entities.skill import Skill

def skill_model_to_entity(model: SkillModel) -> Skill:
    return Skill(
        id=model.id,
        name=model.name,
    )

async def get_all_skills_impl(session):
    result = await session.execute(select(SkillModel))
    models = result.scalars().all()
    return [skill_model_to_entity(m) for m in models]


async def get_skill_by_id_impl(session, skill_id: int):
    result = await session.execute(select(SkillModel).where(SkillModel.id == skill_id))
    model = result.scalar_one_or_none()
    return skill_model_to_entity(model) if model else None

async def get_skill_name_by_id_impl(session, skill_id: int) -> str:
    result = await session.execute(select(SkillModel.name).where(SkillModel.id == skill_id))
    name = result.scalar_one_or_none()
    return name if name else None

async def create_skill_impl(session, skill: Skill):
    model = SkillModel(name=skill.name)
    session.add(model)
    await session.commit()
    await session.refresh(model)
    return skill_model_to_entity(model)

async def update_skill_impl(session, skill: Skill):
    await session.execute(
        sqlalchemy_update(SkillModel)
        .where(SkillModel.id == skill.id)
        .values(name=skill.name)
    )
    await session.commit()
    return await get_skill_by_id_impl(session, skill.id)

async def delete_skill_impl(session, skill_id: int):
    await session.execute(
        sqlalchemy_delete(SkillModel).where(SkillModel.id == skill_id)
    )
    await session.commit()
    return True