from abc import ABC, abstractmethod
from app.domain.entities.filter_match import FilterMatch

class FilterMatchRepository(ABC):
    @abstractmethod
    async def save(self, filter_match: FilterMatch):
        pass

    @abstractmethod
    async def find_by_job_offer_id(self, job_offer_id: int, stage: int) -> FilterMatch:
        pass