from app.domain.entities.agreement import Agreement, AgreementStatus
from app.domain.repositories.agreement_repository import AgreementRepository
from datetime import datetime
from typing import Optional, Dict, Any

class AgreementService:
    def __init__(self, agreement_repo: AgreementRepository):
        self.agreement_repo = agreement_repo

    async def register_agreement(self, agreement_data: Dict[str, Any]) -> int:
        # No permitir manipulación de campos temporales por usuario
        agreement = self.agreement_entity(agreement_data)
        agreement.created_at = datetime.utcnow()
        agreement.updated_at = datetime.utcnow()
        agreement.deleted_at = None
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
            end_date=agreement_data.get("end_date", existing_agreement.end_date),
            created_at=existing_agreement.created_at,  # conservar original
            updated_at=datetime.utcnow(),  # actualizar
            deleted_at=existing_agreement.deleted_at  # conservar
        )
        await self.agreement_repo.update(updated_agreement)
        return updated_agreement
    
    async def delete_agreement(self, agreement_id: int, soft_delete: bool = False) -> bool:
        if soft_delete:
            existing_agreement = await self.agreement_repo.find_by_id(agreement_id)
            if not existing_agreement:
                return False
            # Solo setear deleted_at, conservar el resto
            existing_agreement.deleted_at = datetime.utcnow()
            await self.agreement_repo.update(existing_agreement)
            return True
        else:
            return await self.agreement_repo.delete(agreement_id)
    
    def agreement_entity(self, agreement_data: Dict[str, Any]) -> Agreement:
        # No permitir manipulación de campos temporales por usuario
        return Agreement(
            id=0,  # se asignará automáticamente por la base de datos
            job_offer_id=agreement_data["job_offer_id"],
            student_id=agreement_data["student_id"],
            status=AgreementStatus(agreement_data["status"]),
            start_date=agreement_data.get("start_date"),
            end_date=agreement_data.get("end_date"),
            created_at=None,
            updated_at=None,
            deleted_at=None
        )