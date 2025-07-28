from abc import ABC, abstractmethod
from app.domain.entities.agreement import Agreement

class AgreementPort(ABC):
    @abstractmethod
    async def register_agreement(self, agreement: Agreement) -> Agreement:
        pass

    @abstractmethod
    async def validate_agreement_data(self, agreement_data: dict) -> bool:
        pass

    @abstractmethod
    async def check_agreement_exists(self, student_id: int, job_offer_id: int) -> bool:
        pass

    @abstractmethod
    async def update_agreement_status(self, agreement_id: int, status: str) -> Agreement:
        pass
