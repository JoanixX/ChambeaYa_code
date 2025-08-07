from abc import ABC, abstractmethod
from app.domain.entities.experience_detail import ExperienceDetail
from typing import Optional

class ExperienceDetailRepository(ABC):
    @abstractmethod
    async def save(self, experience_detail: ExperienceDetail) -> ExperienceDetail:
        pass

    @abstractmethod
    async def find_by_id(self, experience_id: int) -> Optional[ExperienceDetail]:
        pass

    @abstractmethod
    async def get_all(self) -> list[ExperienceDetail]:
        pass

    @abstractmethod
    async def delete(self, experience_id: int) -> bool:
        pass

    @abstractmethod
    async def get_name_by_id(self, experience_id: int) -> Optional[str]:
        pass
