from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.job_offer import JobOffer

class JobOfferRepository(ABC):
    @abstractmethod
    async def get_enriched_job_offers(self, session) -> list:
        pass
    
    @abstractmethod
    async def save(self, job_offer: JobOffer):
        pass

    @abstractmethod
    async def find_by_id(self, job_offer_id: int) -> Optional[JobOffer]:
        pass

    @abstractmethod
    async def find_by_company_id(self, company_id: int) -> Optional[JobOffer]:
        pass

    @abstractmethod
    async def get_all(self) -> list[JobOffer]:
        pass

    @abstractmethod
    async def update(self, job_offer: JobOffer):
        pass

    @abstractmethod
    async def delete(self, job_offer_id: int):
        pass