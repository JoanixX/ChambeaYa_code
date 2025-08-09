from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from datetime import datetime

from app.application.ports.agreement_port import AgreementPort
from app.adapters.output.orm.repositories.agreement_repository_impl import AgreementRepositoryImpl
from app.domain.entities.agreement import Agreement, AgreementStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgreementPortImpl(AgreementPort):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.agreement_repo = AgreementRepositoryImpl(session)

    async def register_agreement(self, agreement_data: Dict[str, Any]) -> Agreement:
        if 'created_at' not in agreement_data:
            agreement_data['created_at'] = datetime.now()
        if 'updated_at' not in agreement_data:
            agreement_data['updated_at'] = datetime.now()
        agreement = Agreement(
            id=0,
            job_offer_id=agreement_data['job_offer_id'],
            student_id=agreement_data['student_id'],
            status=agreement_data.get('status', AgreementStatus.pending),
            start_date=agreement_data['start_date'],
            end_date=agreement_data['end_date'],
            created_at=agreement_data['created_at'],
            updated_at=agreement_data['updated_at'],
            deleted_at=agreement_data.get('deleted_at')
        )

        saved_agreement = await self.agreement_repo.save(agreement)
        return saved_agreement

    async def get_agreement(self, agreement_id: int) -> Optional[Agreement]:
        return await self.agreement_repo.find_by_id(agreement_id)
    
    async def check_agreement_exists(self, job_offer_id: int, student_id: int) -> bool:
        agreement = await self.agreement_repo.find_active_agreement(job_offer_id, student_id)
        return agreement is not None
    
    async def get_all_agreements(self) -> list[Agreement]:
        return await self.agreement_repo.get_all()
    
    async def get_student_agreements(self, student_id: int) -> list[Agreement]:
        return await self.agreement_repo.find_by_student_id(student_id)
    
    async def get_job_offer_agreements(self, job_offer_id: int) -> list[Agreement]:
        return await self.agreement_repo.find_by_job_offer_id(job_offer_id)

    async def update_agreement(self, agreement_id: int, agreement_data: Dict[str, Any]) -> Optional[Agreement]:
        existing_agreement = await self.agreement_repo.find_by_id(agreement_id)
        if not existing_agreement:
            return None
        if 'created_at' not in agreement_data:
            agreement_data['created_at'] = existing_agreement.created_at
        if 'updated_at' not in agreement_data:
            agreement_data['updated_at'] = datetime.now()
        
        updated_agreement = Agreement(
            id=agreement_id,
            job_offer_id=agreement_data.get('job_offer_id', existing_agreement.job_offer_id),
            student_id=agreement_data.get('student_id', existing_agreement.student_id),
            status=agreement_data.get('status', existing_agreement.status),
            start_date=agreement_data.get('start_date', existing_agreement.start_date),
            end_date=agreement_data.get('end_date', existing_agreement.end_date),
            created_at=agreement_data['created_at'],
            updated_at=agreement_data['updated_at'],
            deleted_at=agreement_data.get('deleted_at', existing_agreement.deleted_at)
        )

        return await self.agreement_repo.update(updated_agreement)
    
    async def delete_agreement(self, agreement_id: int) -> bool:
        return await self.agreement_repo.delete(agreement_id)
    
    async def validate_agreement_data(self, agreement_data: Dict[str, Any]) -> bool:
        logger.info("Validando datos del acuerdo: {agreement_data}")
        required_fields = ['job_offer_id', 'student_id', 'status', 'start_date', 'end_date']

        for field in required_fields:
            if field not in agreement_data or not agreement_data[field]:
                logger.error(f"Campo faltante o vacío: {field}")
                return False
            
        if agreement_data['start_date'] and agreement_data['end_date']:
            if agreement_data['end_date'] <= agreement_data['start_date']:
                logger.error("La fecha de fin debe ser posterior a la fecha de inicio.")
                return False
        
        logger.info("Validación exitosa")
        return True