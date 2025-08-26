from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.experience_detail import ExperienceDetail

class ExperienceDetailRepository(ABC):
    @abstractmethod
    async def save(self, experience_detail: ExperienceDetail):
        pass

    @abstractmethod
    async def find_by_id(self, experience_detail_id: int) -> Optional[ExperienceDetail]:
        pass

    @abstractmethod
    async def find_by_student_id(self, student_id: int) -> Optional[ExperienceDetail]:
        pass

    @abstractmethod
    async def find_by_job_offer_id(self, job_offer_id: int) -> Optional[ExperienceDetail]:
        pass

    @abstractmethod
    async def get_all(self) -> list[ExperienceDetail]:
        pass

    @abstractmethod
    async def update(self, experience_detail: ExperienceDetail):
        pass

    @abstractmethod
    async def delete(self, experience_detail_id: int):
        pass