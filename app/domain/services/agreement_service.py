from typing import Optional, Dict, Any
from datetime import datetime

from app.domain.entities.agreement import Agreement, AgreementStatus
from app.domain.repositories.agreement_repository import AgreementRepository

class AgreementService:
    def __init__(self, agreement_repo: AgreementRepository):
        self.agreement_repo = agreement_repo

    async def register_agreement(self, agreement_data: Dict[str, Any]) -> int:
        agreement = self.agreement_entity(agreement_data)
        
        saved_model = await self.agreement_repo.save(agreement)
        if saved_model:
            return saved_model.id
        else:
            raise ValueError("Error al guardar el acuerdo")
        
    async def get_agreement(self, agreement_id: int) -> Optional[Agreement]:
        return await self.agreement_repo.find_by_id(agreement_id)
    
    async def find_active_agreement(self, job_offer_id: int, student_id: int) -> Optional[Agreement]:
        agreements = await self.agreement_repo.find_active_agreement(job_offer_id, student_id)
        return agreements[0] if agreements else None

    async def get_student_agreements(self, student_id: int) -> list[Agreement]:
        agreements = await self.agreement_repo.find_by_student_id(student_id)
        return agreements
    
    async def get_job_offer_agreements(self, job_offer_id: int) -> list[Agreement]:
        agreements = await self.agreement_repo.find_by_job_offer_id(job_offer_id)
        return agreements

    async def get_all_agreements(self) -> list[Agreement]:
        return await self.agreement_repo.get_all()

    async def update_agreement(self, agreement_id: int, agreement_data: Dict[str, Any]) -> Optional[Agreement]:
        existing_agreement = await self.agreement_repo.find_by_id(agreement_id)
        if not existing_agreement:
            return None

        updated_agreement = Agreement(
            id=agreement_id,
            job_offer_id=agreement_data.get("job_offer_id", existing_agreement.job_offer_id),
            student_id=agreement_data.get("student_id", existing_agreement.student_id),
            status=AgreementStatus(agreement_data.get("status", existing_agreement.status.value)),
            start_date=agreement_data.get("start_date", existing_agreement.start_date),
            end_date=agreement_data.get("end_date", existing_agreement.end_date)
        )

        await self.agreement_repo.update(updated_agreement)
        return updated_agreement
    
    async def delete_agreement(self, agreement_id: int) -> bool:
        return await self.agreement_repo.delete(agreement_id)
    
    def agreement_entity(self, agreement_data: Dict[str, Any]) -> Agreement:
        if 'created_at' not in agreement_data:
            agreement_data['created_at'] = datetime.now()
        if 'updated_at' not in agreement_data:
            agreement_data['updated_at'] = datetime.now()
        return Agreement(
            id=0,  # se asignará automáticamente por la base de datos
            job_offer_id=agreement_data["job_offer_id"],
            student_id=agreement_data["student_id"],
            status=AgreementStatus(agreement_data["status"]),
            start_date=agreement_data.get("start_date"),
            end_date=agreement_data.get("end_date"),
            created_at=agreement_data['created_at'],
            updated_at=agreement_data['updated_at']
        )