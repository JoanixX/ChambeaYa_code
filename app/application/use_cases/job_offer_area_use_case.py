from app.application.ports.job_offer_area_port import JobOfferAreaPort
from app.domain.entities.job_offer_area import JobOfferArea
from app.domain.services.job_offer_area_service import JobOfferAreaService
from typing import Dict, Any, List

class JobOfferAreaUseCase:
    def __init__(self, job_offer_area_port: JobOfferAreaPort, job_offer_area_service: JobOfferAreaService):
        self.job_offer_area_port = job_offer_area_port
        self.job_offer_area_service = job_offer_area_service

    async def get_job_offer_areas(self, job_offer_id: int) -> List[JobOfferArea]:
        return await self.job_offer_area_port.get_job_offer_areas(job_offer_id)

    async def add_job_offer_area(self, job_offer_area: JobOfferArea) -> JobOfferArea:
        area_id = await self.job_offer_area_port.add_job_offer_area(job_offer_area) 

        if not area_id:
            raise ValueError("Error al agregar el area a la oferta de trabajo")

        return area_id
    
    async def delete_job_offer_area(self, job_offer_id: int, area_id: int) -> Dict[str, Any]:
        success = await self.job_offer_area_port.delete_job_offer_area(job_offer_id, area_id)

        if not success:
            raise ValueError(f"Error al eliminar el area con ID {area_id} de la oferta de trabajo con ID {job_offer_id}")

        return {
            "message": "Área eliminada exitosamente de la oferta de trabajo"
        }