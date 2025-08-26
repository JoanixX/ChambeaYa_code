from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.job_offer_area import JobOfferArea

class JobOfferAreaRepository(ABC):
    @abstractmethod
    def get_by_job_offer_id(self, job_offer_id: int) -> List[JobOfferArea]:
        pass

    @abstractmethod
    def exists(self, job_offer_id: int, area_id: int) -> bool:
        pass

    @abstractmethod
    def save(self, job_offer_area: JobOfferArea) -> JobOfferArea:
        pass

    @abstractmethod
    def delete(self, job_offer_id: int, area_id: int) -> None:
        pass