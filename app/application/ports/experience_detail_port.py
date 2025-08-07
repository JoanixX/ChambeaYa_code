from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.entities.experience_detail import ExperienceDetail

class ExperienceDetailPort(ABC):
    @abstractmethod
    async def register_experience_detail(self, experience_detail: ExperienceDetail) -> ExperienceDetail:
        pass

    @abstractmethod
    async def get_experience_detail(self, experience_detail_id: int) -> Optional[ExperienceDetail]:
        pass

    @abstractmethod
    async def get_all_experience_details(self) -> List[ExperienceDetail]:
        pass

    @abstractmethod
    async def delete_experience_detail(self, experience_detail_id: int) -> bool:
        pass

    @abstractmethod
    async def get_experience_detail_name_by_id(self, experience_detail_id: int) -> Optional[str]:
        pass