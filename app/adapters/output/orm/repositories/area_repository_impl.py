from sqlalchemy.future import select
from app.adapters.output.orm.models.area_model import AreaModel
from app.domain.entities.area import Area

async def get_area_by_id_impl(session, area_id: int):
    result = await session.execute(select(AreaModel).where(AreaModel.id == area_id))
    model = result.scalar_one_or_none()
    return Area(id=model.id, name=model.name) if model else None

async def get_area_name_by_id_impl(session, area_id: int) -> str:
    result = await session.execute(select(AreaModel.name).where(AreaModel.id == area_id))
    name = result.scalar_one_or_none()
    return name if name else None
