from app.domain.entities.job_offer_area import JobOfferArea
from app.domain.repositories.job_offer_area_repository import JobOfferAreaRepository
from typing import List

class JobOfferAreaService:
    def __init__(self, job_offer_area_repo: JobOfferAreaRepository):
        self.job_offer_area_repo = job_offer_area_repo

    async def add_job_offer_area(self, job_offer_area: JobOfferArea) -> JobOfferArea:
        exists = await self.job_offer_area_repo.exists(job_offer_area.job_offer_id, job_offer_area.area_id)

        if exists:
            raise ValueError("La oferta de trabajo ya tiene esta área asignada")

        saved_model = await self.job_offer_area_repo.save(job_offer_area)

        if saved_model:
            return saved_model
        else:
            raise ValueError("Error al guardar el área de la oferta de trabajo")

    async def get_job_offer_areas(self, job_offer_id: int) -> List[JobOfferArea]:
        return await self.job_offer_area_repo.get_by_job_offer_id(job_offer_id)

    async def delete_job_offer_area(self, job_offer_id: int, area_id: int) -> bool:
        return await self.job_offer_area_repo.delete(job_offer_id, area_id)