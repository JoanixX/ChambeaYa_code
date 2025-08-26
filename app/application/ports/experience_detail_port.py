from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

from app.domain.entities.experience_detail import ExperienceDetail

class ExperienceDetailPort(ABC):
    @abstractmethod
    async def register_experience_detail(self, experience_detail_data: Dict[str, Any]) -> ExperienceDetail:
        pass

    @abstractmethod
    async def get_experience_detail(self, experience_detail_id: int) -> Optional[ExperienceDetail]:
        pass

    @abstractmethod
    async def get_experience_details_by_student_id(self, student_id: int) -> Optional[ExperienceDetail]:
        pass

    @abstractmethod
    async def get_experience_details_by_job_offer_id(self, job_offer_id: int) -> Optional[ExperienceDetail]:
        pass

    @abstractmethod
    async def get_all_experience_details(self) -> List[ExperienceDetail]:
        pass

    @abstractmethod
    async def update_experience_detail(self, experience_detail_id: int, experience_detail_data: Dict[str, Any]) -> Optional[ExperienceDetail]:
        pass

    @abstractmethod
    async def delete_experience_detail(self, experience_detail_id: int) -> bool:
        pass