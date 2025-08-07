from typing import Optional, List, Dict, Any

from app.application.ports.experience_detail_port import ExperienceDetailPort
from app.domain.services.experience_detail_service import ExperienceDetailService
from app.adapters.input.fastapi.schemas.experience_detail_schema import ExperienceDetailResponse

class ExperienceDetailUseCase:
    def __init__(self, experience_detail_port: ExperienceDetailPort, experience_detail_service: ExperienceDetailService):
        self.experience_detail_port = experience_detail_port
        self.experience_detail_service = experience_detail_service

    async def register_experience_detail(self, experience_detail_data: Dict[str, Any]) -> int:
        experience_detail_id = await self.experience_detail_service.register_experience_detail(experience_detail_data)

        if not experience_detail_id:
            raise ValueError("Error al guardar el área")

        return experience_detail_id

    async def get_all_experience_details(self) -> List[ExperienceDetailResponse]:
        experience_details = await self.experience_detail_port.get_all_experience_details()
        return [ExperienceDetailResponse(id=a.id, name=a.name) for a in experience_details]
    
    async def get_experience_detail(self, experience_detail_id: int) -> ExperienceDetailResponse:
        experience_detail = await self.experience_detail_port.get_experience_detail(experience_detail_id)
        if not experience_detail:
            raise ValueError(f"Área con ID {experience_detail_id} no encontrada")
        return ExperienceDetailResponse(id=experience_detail.id, name=experience_detail.name)
    
    async def delete_experience_detail(self, experience_detail_id: int) -> Dict[str, Any]:
        experience_detail = await self.experience_detail_port.get_experience_detail(experience_detail_id)
        if not experience_detail:
            raise ValueError(f"Área con ID {experience_detail_id} no encontrada")

        success = await self.experience_detail_port.delete_experience_detail(experience_detail_id)
        if not success:
            raise ValueError(f"Error al eliminar área con ID {experience_detail_id}")

        return {
            "message": "Área eliminada exitosamente"
        }
    
    async def get_experience_detail_name_by_id(self, experience_detail_id: int) -> Optional[str]:
        experience_detail_name = await self.experience_detail_port.get_experience_detail_name_by_id(experience_detail_id)
        if not experience_detail_name:
            raise ValueError(f"Área con ID {experience_detail_id} no encontrada")
        return experience_detail_name