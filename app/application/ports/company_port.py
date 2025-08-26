from abc import ABC, abstractmethod
from app.domain.entities.company import Company
from typing import Optional, Dict, Any, List

class CompanyPort(ABC):
    @abstractmethod
    async def register_company(self, company_data: Dict[str, Any]) -> Company:
        pass

    @abstractmethod
    async def get_company(self, company_id: int) -> Optional[Company]:
        pass

    @abstractmethod
    async def get_all_companies(self) -> List[Company]:
        pass

    @abstractmethod
    async def update_company(self, company_id: int, company_data: Dict[str, Any]) -> Optional[Company]:
        pass

    @abstractmethod
    async def delete_company(self, company_id: int) -> bool:
        pass

    @abstractmethod
    async def validate_company_data(self, company_data: Dict[str, Any]) -> bool:
        pass