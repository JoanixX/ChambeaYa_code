from abc import ABC, abstractmethod
from app.domain.entities.agreement import Agreement
from typing import Optional

class AgreementRepository(ABC):
    @abstractmethod
    async def save(self, agreement: Agreement):
        pass

    @abstractmethod
    async def find_by_id(self, agreement_id: int) -> Optional[Agreement]:
        pass

    @abstractmethod
    async def find_by_student_id(self, student_id: int) -> list[Agreement]:
        pass

    @abstractmethod
    async def find_by_job_offer_id(self, job_offer_id: int) -> list[Agreement]:
        pass

    @abstractmethod
    async def find_active_agreement(self, job_offer_id: int, student_id: int) -> list[Agreement]:
        pass

    @abstractmethod
    async def get_all(self) -> list[Agreement]:
        pass

    @abstractmethod
    async def update(self, agreement: Agreement):
        pass

    @abstractmethod
    async def delete(self, agreement_id: int):
        pass
