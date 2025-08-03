from app.domain.entities.job_offer import JobOffer
from app.domain.repositories.job_offer_repository import JobOfferRepository
from typing import Dict, Any, Optional

class JobOfferService:
    async def get_enriched_job_offers(self) -> list:
        return await self.job_offer_repo.get_enriched_job_offers(self.job_offer_repo.session)
    def __init__(self, job_offer_repo: JobOfferRepository):
        self.job_offer_repo = job_offer_repo

    async def register_job_offer(self, job_offer_data: Dict[str, Any]) -> int:
        job_offer = self.job_offer_entity(job_offer_data)

        saved_model = await self.job_offer_repo.save(job_offer)
        if saved_model:
            return saved_model.id
        else:
            raise ValueError("Error al guardar la oferta de trabajo")
        
    async def get_job_offer(self, job_offer_id: int) -> Optional[JobOffer]:
        return await self.job_offer_repo.find_by_id(job_offer_id)
    
    async def get_all_job_offers(self) -> list[JobOffer]:
        return await self.job_offer_repo.get_all()
    
    async def update_job_offer(self, job_offer_id: int, job_offer_data: Dict[str, Any]) -> Optional[JobOffer]:
        existing_job_offer = await self.job_offer_repo.find_by_id(job_offer_id)
        if not existing_job_offer:
            return None

        updated_job_offer = JobOffer(
            id=job_offer_id,
            company_id=job_offer_data.get("company_id", existing_job_offer.company_id),
            title=job_offer_data.get("title", existing_job_offer.title),
            description=job_offer_data.get("description", existing_job_offer.description),
            required_hours=job_offer_data.get("required_hours", existing_job_offer.required_hours),
            approximated_salary=job_offer_data.get("approximated_salary", existing_job_offer.approximated_salary),
            duration=job_offer_data.get("duration", existing_job_offer.duration),
            start_date=job_offer_data.get("start_date", existing_job_offer.start_date),
            area_id=job_offer_data.get("area_id", existing_job_offer.area_id),
            experience_id=job_offer_data.get("experience_id", existing_job_offer.experience_id),
            modality=job_offer_data.get("modality", existing_job_offer.modality),
            embedding=job_offer_data.get("embedding", existing_job_offer.embedding)
        )

        await self.job_offer_repo.update(updated_job_offer)
        return updated_job_offer
    
    async def delete_job_offer(self, job_offer_id: int) -> bool:
        return await self.job_offer_repo.delete(job_offer_id)
    
    def job_offer_entity(self, job_offer_data: Dict[str, Any]) -> JobOffer:
        return JobOffer(
            id=0,
            company_id=job_offer_data.get("company_id", None),
            title=job_offer_data.get("title", None),
            description=job_offer_data.get("description", None),
            required_hours=job_offer_data.get("required_hours", None),
            approximated_salary=job_offer_data.get("approximated_salary", None),
            duration=job_offer_data.get("duration", None),
            start_date=job_offer_data.get("start_date", None),
            area_id=job_offer_data.get("area_id", None),
            experience_id=job_offer_data.get("experience_id", None),
            modality=job_offer_data.get("modality", None),
            embedding=job_offer_data.get("embedding", {})
        )