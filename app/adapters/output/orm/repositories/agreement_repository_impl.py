from app.domain.repositories.agreement_repository import AgreementRepository
from app.domain.entities.agreement import Agreement, AgreementStatus
from app.adapters.output.orm.models.agreement_model import AgreementModel, AgreementStatus as AgreementStatusModel
from sqlalchemy.future import select
from sqlalchemy import delete
from typing import Optional

class AgreementRepositoryImpl(AgreementRepository):
    def __init__(self, session):
        self.session = session

    async def save(self, agreement: Agreement):
        model = AgreementModel(
            job_offer_id=agreement.job_offer_id,
            student_id=agreement.student_id,
            status=agreement.status.value,
            start_date=agreement.start_date,
            end_date=agreement.end_date
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def find_by_id(self, agreement_id: int) -> Optional[Agreement]:
        result = await self.session.execute(select(AgreementModel).where(AgreementModel.id == agreement_id))
        model = result.scalar_one_or_none()
        if model:
            return Agreement(
                id=model.id,
                job_offer_id=model.job_offer_id,
                student_id=model.student_id,
                status=AgreementStatus(model.status),  # Convertir desde el valor
                start_date=model.start_date,
                end_date=model.end_date,
                created_at=model.created_at,
                updated_at=model.updated_at,
                deleted_at=model.deleted_at
            )
        return None

    async def find_by_student_id(self, student_id: int) -> list[Agreement]:
        result = await self.session.execute(select(AgreementModel).where(AgreementModel.student_id == student_id))
        models = result.scalars().all()
        agreements = []
        for model in models:
            agreements.append(Agreement(
                id=model.id,
                job_offer_id=model.job_offer_id,
                student_id=model.student_id,
                status=AgreementStatus(model.status),  # Convertir desde el valor
                start_date=model.start_date,
                end_date=model.end_date,
                created_at=model.created_at,
                updated_at=model.updated_at,
                deleted_at=model.deleted_at
            ))
        return agreements

    async def find_by_job_offer_id(self, job_offer_id: int) -> list[Agreement]:
        result = await self.session.execute(select(AgreementModel).where(AgreementModel.job_offer_id == job_offer_id))
        models = result.scalars().all()
        agreements = []
        for model in models:
            agreements.append(Agreement(
                id=model.id,
                job_offer_id=model.job_offer_id,
                student_id=model.student_id,
                status=AgreementStatus(model.status),  # Convertir desde el valor
                start_date=model.start_date,
                end_date=model.end_date,
                created_at=model.created_at,
                updated_at=model.updated_at,
                deleted_at=model.deleted_at
            ))
        return agreements

    async def find_active_agreement (self, job_offer_id: int, student_id: int) -> Optional[Agreement]:
        result = await self.session.execute(select(AgreementModel).
        where(AgreementModel.job_offer_id == job_offer_id, AgreementModel.student_id 
        == student_id, AgreementModel.status == AgreementStatusModel.active))

        model = result.scalar_one_or_none()
        if model:
            return Agreement(
                id=model.id,
                job_offer_id=model.job_offer_id,
                student_id=model.student_id,
                status=AgreementStatus(model.status),  # Convertir desde el valor
                start_date=model.start_date,
                end_date=model.end_date,
                created_at=model.created_at,
                updated_at=model.updated_at,
                deleted_at=model.deleted_at
            )
        return None

    async def get_all(self) -> list[Agreement]:
        result = await self.session.execute(select(AgreementModel))
        models = result.scalars().all()
        agreements = []
        for model in models:
            agreements.append(Agreement(
                id=model.id,
                job_offer_id=model.job_offer_id,
                student_id=model.student_id,
                status=AgreementStatus(model.status),  # Convertir desde el valor
                start_date=model.start_date,
                end_date=model.end_date,
                created_at=model.created_at,
                updated_at=model.updated_at,
                deleted_at=model.deleted_at
            ))
        return agreements

    async def update(self, agreement: Agreement):
        result = await self.session.execute(select(AgreementModel).where(AgreementModel.id == agreement.id))
        model = result.scalar_one_or_none()
        if model:
            model.job_offer_id = agreement.job_offer_id
            model.student_id = agreement.student_id
            model.status = agreement.status.value  # Usar el valor directamente
            model.start_date = agreement.start_date
            model.end_date = agreement.end_date
            await self.session.commit()
            await self.session.refresh(model)
            return agreement
        return None
    
    async def delete(self, agreement_id: int):
        result = await self.session.execute(select(AgreementModel).where(AgreementModel.id == agreement_id))
        model = result.scalar_one_or_none()
        if not model:
            return False

        await self.session.execute(delete(AgreementModel).where(AgreementModel.id == agreement_id))
        await self.session.commit()
        return True
