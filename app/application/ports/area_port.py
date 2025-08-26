from abc import ABC, abstractmethod
from app.domain.entities.area import Area
from typing import Optional, Dict, Any, List

class AreaPort(ABC):
    @abstractmethod
    async def register_area(self, area_data: Dict[str, Any]) -> Area:
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