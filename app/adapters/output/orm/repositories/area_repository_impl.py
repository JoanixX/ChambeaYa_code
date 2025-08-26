from sqlalchemy.future import select
from sqlalchemy import delete
from typing import Optional
from app.adapters.output.orm.models.area_model import AreaModel
from app.domain.entities.area import Area
from app.domain.repositories.area_repository import AreaRepository

class AreaRepositoryImpl(AreaRepository):
    def __init__(self, session):
        self.session = session
    
    async def save(self, area: Area):
        model = AreaModel(
            name=area.name
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model
    
    async def find_by_id(self, area_id: int) -> Optional[Area]:
        result = await self.session.execute(select(AreaModel).where(AreaModel.id == area_id))
        model = result.scalar_one_or_none()
        if model:
            return Area(
                id=model.id,
                name=model.name
            )
        return None
    
    async def get_all(self) -> list[Area]:
        result = await self.session.execute(select(AreaModel))
        models = result.scalars().all()
        areas = []
        for model in models:
            areas.append(
                Area(
                    id=model.id,
                    name=model.name
                )
            )
        return areas
    
    async def delete(self, area_id: int) -> bool:
        result = await self.session.execute(select(AreaModel).where(AreaModel.id == area_id))
        model = result.scalar_one_or_none()
        if not model:
            return False

        await self.session.execute(delete(AreaModel).where(AreaModel.id == area_id))
        await self.session.commit()
        return True
    
    async def get_name_by_id(self, area_id: int) -> Optional[str]:
        result = await self.session.execute(select(AreaModel.name).where(AreaModel.id == area_id))
        name = result.scalar_one_or_none()
        return name if name else None