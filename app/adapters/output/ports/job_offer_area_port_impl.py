from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.job_offer_area import JobOfferArea
from app.adapters.output.orm.repositories.job_offer_area_repository_impl import JobOfferAreaRepositoryImpl
from app.application.ports.job_offer_area_port import JobOfferAreaPort

class JobOfferAreaPortImpl(JobOfferAreaPort):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.job_offer_area_repo = JobOfferAreaRepositoryImpl(session)

    async def add_job_offer_area(self, job_offer_area: JobOfferArea) -> JobOfferArea:
        return await self.job_offer_area_repo.save(job_offer_area)

    async def get_job_offer_areas(self, job_offer_id: int) -> List[JobOfferArea]:
        return await self.job_offer_area_repo.get_by_job_offer_id(job_offer_id)
    
    async def delete_job_offer_area(self, job_offer_id: int, area_id: int) -> bool:
        return await self.job_offer_area_repo.delete(job_offer_id, area_id)
    
    async def job_offer_area_exists(self, job_offer_id: int, area_id: int) -> bool:
        return await self.job_offer_area_repo.exists(job_offer_id, area_id)