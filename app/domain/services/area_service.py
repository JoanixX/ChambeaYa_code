from app.domain.entities.area import Area
from app.domain.repositories.area_repository import AreaRepository
from typing import Dict, Any, Optional

class AreaService:
    def __init__(self, area_repo: AreaRepository):
        self.area_repo = area_repo

    async def register_area(self, area_data: Dict[str, Any]) -> int:
        area = Area(
            id=0,
            name=area_data["name"],
            description=area_data.get("description", "")
        )
        saved_model = await self.area_repo.save(area)
        if saved_model:
            return saved_model.id
        else:
            raise ValueError("Error al guardar el área")
    
    async def get_area(self, area_id: int) -> Optional[Area]:
        return await self.area_repo.find_by_id(area_id)
    
    async def get_all_areas(self) -> list[Area]:
        return await self.area_repo.get_all()
    
    async def delete_area(self, area_id: int) -> bool:
        return await self.area_repo.delete(area_id)
    
    async def get_name_by_id(self, area_id: int) -> Optional[str]:
        return await self.area_repo.get_name_by_id(area_id)