from abc import ABC, abstractmethod
from app.domain.entities.interest import Interest
from typing import Optional

class InterestRepository(ABC):
    @abstractmethod
    async def save(self, interest: Interest):
        pass

    @abstractmethod
    async def find_by_id(self, interest_id: int) -> Optional[Interest]:
        pass

    @abstractmethod
    async def get_all(self) -> list[Interest]:
        pass

    @abstractmethod
    async def delete(self, interest_id: int):
        pass

    @abstractmethod
    async def get_name_by_id(self, interest_id: int) -> Optional[str]:
        pass