from abc import ABC, abstractmethod
from app.domain.entities.filter_match import FilterMatch
from typing import Dict, Any

class FilterMatchPort(ABC):
    @abstractmethod
    async def preprocess_job_offer(self, job_offer_id: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def preprocess_all_job_offers(self, job_offer_ids: list[int]) -> list[Dict[str, Any]]:
        pass

    @abstractmethod
    async def preprocess_student(self, student_id: int) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def preprocess_all_students(self, student_ids: list[int]) -> list[Dict[str, Any]]:
        pass

    @abstractmethod
    async def register_filter_match_student(self, 
        student_id: int, filter_match_data: Dict[str, Any]) -> FilterMatch:
        pass

    @abstractmethod
    async def register_filter_match_job_offer(self, 
        job_offer_id: int, filter_match_data: Dict[str, Any]) -> FilterMatch:
        pass