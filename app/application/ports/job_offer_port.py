from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List

from app.domain.entities.job_offer import JobOffer

class JobOfferPort(ABC):
    @abstractmethod
    async def get_enriched_job_offers(self) -> List[JobOffer]:
        pass

    @abstractmethod
    async def register_job_offer(self, job_offer_data: Dict[str, Any]) -> JobOffer:
        pass

    @abstractmethod
    async def get_job_offer(self, job_offer_id: int) -> Optional[JobOffer]:
        pass
    
    @abstractmethod
    async def get_job_offers_by_company_id(self, company_id: int) -> Optional[JobOffer]:
        pass

    @abstractmethod
    async def get_all_job_offers(self) -> List[JobOffer]:
        pass

    @abstractmethod
    async def update_job_offer(self, job_offer_id: int, job_offer_data: Dict[str, Any]) -> Optional[JobOffer]:
        pass

    @abstractmethod
    async def delete_job_offer(self, job_offer_id: int) -> bool:
        pass

    @abstractmethod
    async def validate_job_offer_data(self, job_offer_data: Dict[str, Any]) -> bool:
        pass