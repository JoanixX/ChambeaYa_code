from typing import Dict, Any, List

from app.domain.entities.experience_detail import ExperienceDetail
from app.application.ports.experience_detail_port import ExperienceDetailPort
from app.domain.services.experience_detail_service import ExperienceDetailService

class ExperienceDetailUseCase:
    def __init__(self, experience_detail_port: ExperienceDetailPort, experience_detail_service: ExperienceDetailService):
        self.experience_detail_port = experience_detail_port
        self.experience_detail_service = experience_detail_service

    async def register_experience_detail(self, experience_detail_data: Dict[str, Any]) -> Dict[str, Any]:
        experience_detail_id = await self.experience_detail_service.register_experience_detail(experience_detail_data)
        
        if not experience_detail_id:
            raise ValueError("Error al guardar experiencia")

        return {
            "id": experience_detail_id,
            "registration_success": True,
            "message": "Experiencia registrada exitosamente"
        }

    async def get_experience_detail(self, experience_detail_id: int) -> ExperienceDetail:
        experience_detail = await self.experience_detail_port.get_experience_detail(experience_detail_id)
        if not experience_detail:
            raise ValueError(f"Experiencia con ID {experience_detail_id} no encontrada")
        return experience_detail

    async def get_student_experience_details(self, student_id: int) -> List[ExperienceDetail]:
        experience_detail = await self.experience_detail_port.get_experience_details_by_student_id(student_id)
        if not experience_detail:
            raise ValueError(f"No se encontraron experiencias para el estudiante con ID {student_id}")
        return experience_detail

    async def get_job_offer_experience_details(self, job_offer_id: int) -> List[ExperienceDetail]:
        experience_detail = await self.experience_detail_port.get_experience_details_by_job_offer_id(job_offer_id)
        if not experience_detail:
            raise ValueError(f"No se encontraron experiencias para la oferta de trabajo con ID {job_offer_id}")
        return experience_detail

    async def get_all_experience_details(self) -> List[ExperienceDetail]:
        return await self.experience_detail_port.get_all_experience_details()

    async def update_experience_detail(self, experience_detail_id: int, experience_detail_data: Dict[str, Any]) -> ExperienceDetail:
        experience_detail = await self.experience_detail_port.get_experience_detail(experience_detail_id)
        if not experience_detail:
            raise ValueError(f"Experiencia con ID {experience_detail_id} no encontrada")

        updated_experience_detail = await self.experience_detail_port.update_experience_detail(experience_detail_id, experience_detail_data)
        if not updated_experience_detail:
            raise ValueError(f"Error al actualizar la experiencia con ID {experience_detail_id}")

        return updated_experience_detail

    async def delete_experience_detail(self, experience_detail_id: int) -> Dict[str, Any]:
        experience_detail = await self.experience_detail_port.get_experience_detail(experience_detail_id)
        if not experience_detail:
            raise ValueError(f"Experiencia con ID {experience_detail_id} no encontrada")

        success = await self.experience_detail_port.delete_experience_detail(experience_detail_id)
        if not success:
            raise ValueError(f"Error al eliminar la experiencia con ID {experience_detail_id}")

        return {
            "message": "Experiencia eliminada exitosamente"
        }