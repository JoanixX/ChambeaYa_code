from abc import ABC, abstractmethod
from app.domain.entities.area import Area
from typing import Optional

class AreaRepository(ABC):
    @abstractmethod
    async def save(self, area: Area):
        pass

    @abstractmethod
    async def find_by_id(self, area_id: int) -> Optional[Area]:
        pass

    @abstractmethod
    async def get_all(self) -> list[Area]:
        pass

    @abstractmethod
    async def delete(self, area_id: int):
        pass

    @abstractmethod
    async def get_name_by_id(self, area_id: int) -> Optional[str]:
        pass