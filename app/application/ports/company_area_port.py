from abc import ABC, abstractmethod
from app.domain.entities.company_area import CompanyArea
from typing import List

class CompanyAreaPort(ABC):
    @abstractmethod
    async def get_company_areas(self, company_id: int) -> List[CompanyArea]:
        pass

    @abstractmethod
    async def add_company_area(self, company_area: CompanyArea) -> CompanyArea:
        pass

    @abstractmethod
    async def delete_company_area(self, company_id: int, area_id: int) -> bool:
        pass