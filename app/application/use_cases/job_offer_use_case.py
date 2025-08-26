from typing import Dict, Any, List

from app.domain.entities.job_offer import JobOffer
from app.application.ports.job_offer_port import JobOfferPort
from app.domain.services.job_offer_service import JobOfferService

class JobOfferUseCase:
    def __init__(self, job_offer_port: JobOfferPort, job_offer_service: JobOfferService):
        self.job_offer_port = job_offer_port
        self.job_offer_service = job_offer_service

    async def get_enriched_job_offers(self) -> List[JobOffer]:
        return await self.job_offer_port.get_enriched_job_offers()

    async def register_job_offer(self, job_offer_data: Dict[str, Any]) -> Dict[str, Any]:
        if not await self.job_offer_port.validate_job_offer_data(job_offer_data):
            raise ValueError("Datos de oferta de trabajo inválidos")

        job_offer_id = await self.job_offer_service.register_job_offer(job_offer_data)
        
        if not job_offer_id:
            raise ValueError("Error al guardar la oferta de trabajo")

        return {
            "id": job_offer_id,
            "registration_success": True,
            "message": "Oferta de trabajo registrada exitosamente"
        }
    
    async def get_job_offer(self, job_offer_id: int) -> JobOffer:
        job_offer = await self.job_offer_port.get_job_offer(job_offer_id)
        if not job_offer:
            raise ValueError(f"Oferta de trabajo con ID {job_offer_id} no encontrada")
        return job_offer
    
    async def get_company_job_offers(self, company_id: int) -> List[JobOffer]:
        job_offer = await self.job_offer_port.get_job_offers_by_company_id(company_id)
        if not job_offer:
            raise ValueError(f"No se encontraron ofertas de trabajo para la empresa con ID {company_id}")
        return job_offer

    async def get_all_job_offers(self) -> List[JobOffer]:
        return await self.job_offer_port.get_all_job_offers()
    
    async def update_job_offer(self, job_offer_id: int, job_offer_data: Dict[str, Any]) -> JobOffer:
        if not await self.job_offer_port.validate_job_offer_data(job_offer_data):
            raise ValueError("Datos de oferta de trabajo inválidos")

        job_offer = await self.job_offer_port.get_job_offer(job_offer_id)
        if not job_offer:
            raise ValueError(f"Oferta de trabajo con ID {job_offer_id} no encontrada")

        updated_job_offer = await self.job_offer_port.update_job_offer(job_offer_id, job_offer_data)
        if not updated_job_offer:
            raise ValueError(f"Error al actualizar la oferta de trabajo con ID {job_offer_id}")

        return updated_job_offer
    
    async def delete_job_offer(self, job_offer_id: int) -> Dict[str, Any]:
        job_offer = await self.job_offer_port.get_job_offer(job_offer_id)
        if not job_offer:
            raise ValueError(f"Oferta de trabajo con ID {job_offer_id} no encontrada")

        success = await self.job_offer_port.delete_job_offer(job_offer_id)
        if not success:
            raise ValueError(f"Error al eliminar la oferta de trabajo con ID {job_offer_id}")

        return {
            "message": "Oferta de trabajo eliminada exitosamente"
        }