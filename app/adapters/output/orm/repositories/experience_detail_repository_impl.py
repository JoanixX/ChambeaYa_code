from sqlalchemy.future import select
from app.adapters.output.orm.models.experience_detail_model import ExperienceDetailModel
from app.domain.entities.experience_detail import ExperienceDetail

async def get_experience_detail_by_id_impl(session, experience_id: int):
    result = await session.execute(select(ExperienceDetailModel).where(ExperienceDetailModel.id == experience_id))
    model = result.scalar_one_or_none()
    return ExperienceDetail(
        id=model.id,
        name=model.name,
        description=model.description,
        duration_in_months=model.duration_in_months
    ) if model else None

async def get_experience_name_by_id_impl(session, experience_id: int) -> str:
    result = await session.execute(select(ExperienceDetailModel.name).where(ExperienceDetailModel.id == experience_id))
    name = result.scalar_one_or_none()
    return name if name else None
