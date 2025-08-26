from typing import Optional, List, Dict, Any

from app.domain.entities.area import Area
from app.application.ports.area_port import AreaPort
from app.domain.services.area_service import AreaService
from app.adapters.input.fastapi.schemas.area_schema import AreaResponse

class AreaUseCase:
    def __init__(self, area_port: AreaPort, area_service: AreaService):
        self.area_port = area_port
        self.area_service = area_service

    async def register_area(self, area_data: Dict[str, Any]) -> int:
        area_id = await self.area_service.register_area(area_data)

        if not area_id:
            raise ValueError("Error al guardar el área")

        return area_id

    async def get_all_areas(self) -> List[Area]:
        areas = await self.area_port.get_all_areas()
        return [AreaResponse(id=a.id, name=a.name) for a in areas]
    
    async def get_area(self, area_id: int) -> Area:
        area = await self.area_port.get_area(area_id)
        if not area:
            raise ValueError(f"Área con ID {area_id} no encontrada")
        return AreaResponse(id=area.id, name=area.name)
    
    async def delete_area(self, area_id: int) -> dict:
        area = await self.area_port.get_area(area_id)
        if not area:
            raise ValueError(f"Área con ID {area_id} no encontrada")

        success = await self.area_port.delete_area(area_id)
        if not success:
            raise ValueError(f"Error al eliminar área con ID {area_id}")

        return {
            "message": "Área eliminada exitosamente"
        }
    
    async def get_area_name_by_id(self, area_id: int) -> Optional[str]:
        area_name = await self.area_port.get_area_name_by_id(area_id)
        if not area_name:
            raise ValueError(f"Área con ID {area_id} no encontrada")
        return area_name