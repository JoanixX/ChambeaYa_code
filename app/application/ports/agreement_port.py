from abc import ABC, abstractmethod
from app.domain.entities.agreement import Agreement
from typing import Dict, Any, Optional

class AgreementPort(ABC):
    @abstractmethod
    async def register_agreement(self, agreement_data: Dict[str, Any]) -> Agreement:
        pass

    @abstractmethod
    async def get_agreement(self, agreement_id: int) -> Optional[Agreement]:
        pass

    @abstractmethod
    async def get_student_agreements(self, student_id: int) -> list[Agreement]:
        pass

    @abstractmethod
    async def get_job_offer_agreements(self, job_offer_id: int) -> list[Agreement]:
        pass

    @abstractmethod
    async def get_all_agreements(self) -> list[Agreement]:
        pass

    @abstractmethod
    async def update_agreement(self, agreement_id: int, agreement_data: Dict[str, Any]) -> Optional[Agreement]:
        pass

    @abstractmethod
    async def delete_agreement(self, agreement_id: int) -> bool:
        pass

    @abstractmethod
    async def validate_agreement_data(self, agreement_data: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    async def check_agreement_exists(self, student_id: int, job_offer_id: int) -> bool:
        pass