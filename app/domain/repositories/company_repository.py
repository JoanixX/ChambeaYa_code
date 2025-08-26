from abc import ABC, abstractmethod
from app.domain.entities.company import Company
from typing import Optional

class CompanyRepository(ABC):
    @abstractmethod
    async def save(self, company: Company):
        pass

    @abstractmethod
    async def find_by_id(self, company_id: int) -> Optional[Company]:
        pass

    @abstractmethod
    async def get_all(self) -> list[Company]:
        pass

    @abstractmethod
    async def update(self, company: Company):
        pass

    @abstractmethod
    async def delete(self, company_id: int):
        pass
