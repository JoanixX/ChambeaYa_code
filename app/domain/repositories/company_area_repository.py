from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.company_area import CompanyArea

class CompanyAreaRepository(ABC):
    @abstractmethod
    def get_by_company_id(self, company_id: int) -> List[CompanyArea]:
        pass

    @abstractmethod
    def exists(self, company_id: int, area_id: int) -> bool:
        pass

    @abstractmethod
    def save(self, company_area: CompanyArea) -> CompanyArea:
        pass

    @abstractmethod
    def delete(self, company_id: int, area_id: int) -> None:
        pass