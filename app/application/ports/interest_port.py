from abc import ABC, abstractmethod
from app.domain.entities.interest import Interest
from typing import Optional, Dict, Any, List

class InterestPort(ABC):
    @abstractmethod
    async def register_interest(self, interest_data: Dict[str, Any]) -> Interest:
        pass

    @abstractmethod
    async def get_interest(self, interest_id: int) -> Optional[Interest]:
        pass

    @abstractmethod
    async def get_all_interests(self) -> List[Interest]:
        pass

    @abstractmethod
    async def delete_interest(self, interest_id: int) -> bool:
        pass