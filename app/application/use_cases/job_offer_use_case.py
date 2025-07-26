from app.domain.entities.job_offer import JobOffer
from app.domain.repositories.job_offer_repository import JobOfferRepository
from typing import Optional, List

class JobOfferUseCase:
    def __init__(self, job_offer_repository: JobOfferRepository):
        self.job_offer_repository = job_offer_repository

    async def get_by_id(self, job_offer_id: int) -> Optional[JobOffer]:
        return await self.job_offer_repository.find_by_id(job_offer_id)

    async def get_all(self) -> List[JobOffer]:
        return await self.job_offer_repository.get_all()

    async def create(self, job_offer: JobOffer) -> Optional[JobOffer]:
        return await self.job_offer_repository.save(job_offer)

    async def update(self, job_offer: JobOffer) -> Optional[JobOffer]:
        return await self.job_offer_repository.update(job_offer)

    async def delete(self, job_offer_id: int):
        await self.job_offer_repository.delete(job_offer_id)
