from typing import Dict, Any, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.output.orm.repositories.area_repository_impl import AreaRepositoryImpl
from app.application.ports.area_port import AreaPort
from app.domain.entities.area import Area

class AreaPortImpl(AreaPort):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.area_repo = AreaRepositoryImpl(session)

    async def register_area(self, area_data: Dict[str, Any]) -> Area:
        area = Area(
            id=0,
            name=area_data["name"]
        )

        saved_area = await self.area_repo.save(area)
        return saved_area

    async def get_area(self, area_id: int) -> Optional[Area]:
        return await self.area_repo.find_by_id(area_id)

    async def get_all_areas(self) -> List[Area]:
        return await self.area_repo.get_all()

    async def delete_area(self, area_id: int) -> bool:
        return await self.area_repo.delete(area_id)
    
    async def get_area_name_by_id(self, area_id: int) -> Optional[str]:
        return await self.area_repo.get_name_by_id(area_id)