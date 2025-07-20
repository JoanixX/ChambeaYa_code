from abc import ABC, abstractmethod
from app.domain.entities.company import Company

class RegisterCompanyPort(ABC):
    @abstractmethod
    async def register_company(self, company: Company) -> Company:
        pass

    @abstractmethod
    async def validate_company_data(self, company_data: dict) -> bool:
        pass

    @abstractmethod
    async def check_ruc_exists(self, ruc: str) -> bool:
        pass

    @abstractmethod
    async def check_email_exists(self, email: str) -> bool:
        pass
