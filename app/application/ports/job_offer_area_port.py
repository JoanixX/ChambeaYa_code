from abc import ABC, abstractmethod
from app.domain.entities.job_offer_area import JobOfferArea
from typing import List

class JobOfferAreaPort(ABC):
    @abstractmethod
    async def get_job_offer_areas(self, job_offer_id: int) -> List[JobOfferArea]:
        pass

    @abstractmethod
    async def add_job_offer_area(self, job_offer_area: JobOfferArea) -> JobOfferArea:
        pass

    @abstractmethod
    async def delete_job_offer_area(self, job_offer_id: int, area_id: int) -> bool:
        pass