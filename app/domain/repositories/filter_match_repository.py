from abc import ABC, abstractmethod
from app.domain.entities.filter_match import FilterMatch

class FilterMatchRepository(ABC):
    @abstractmethod
    async def preprocess_all_job_offers(self, job_offer_ids: list[int]) -> list[dict]:
        pass

    @abstractmethod
    async def preprocess_job_offer(self, job_offer_id: int) -> dict:
        pass

    @abstractmethod
    async def preprocess_all_students(self, student_ids: list[int]) -> list[dict]:
        pass

    @abstractmethod
    async def preprocess_student(self, student_id: int) -> dict:
        pass

    @abstractmethod
    def save_filtered_student(self, student_id: int, filter_match: FilterMatch):
        pass

    @abstractmethod
    def save_filtered_job_offer(self, job_offer_id: int, filter_match: FilterMatch):
        pass