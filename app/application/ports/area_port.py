from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.entities.area import Area

class AreaPort(ABC):
    @abstractmethod
    async def register_area(self, area: Area) -> Area:
        pass

    @abstractmethod
    async def get_area(self, area_id: int) -> Optional[Area]:
        pass

    @abstractmethod
    async def get_all_areas(self) -> List[Area]:
        pass

    @abstractmethod
    async def delete_area(self, area_id: int) -> bool:
        pass

    @abstractmethod
    async def get_area_name_by_id(self, area_id: int) -> Optional[str]:
        pass