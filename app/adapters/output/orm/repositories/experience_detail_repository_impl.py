from sqlalchemy.future import select
from sqlalchemy import delete
from typing import Optional

from app.domain.repositories.experience_detail_repository import ExperienceDetailRepository
from app.domain.entities.experience_detail import ExperienceDetail
from app.adapters.output.orm.models.experience_detail_model import ExperienceDetailModel

class ExperienceDetailRepositoryImpl(ExperienceDetailRepository):
    def __init__(self, session):
        self.session = session

    async def save(self, experience_detail: ExperienceDetail):
        model = ExperienceDetailModel(
            student_id=experience_detail.student_id,
            job_offer_id=experience_detail.job_offer_id,
            name=experience_detail.name,
            description=experience_detail.description,
            duration_in_months=experience_detail.duration_in_months
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def find_by_id(self, experience_detail_id: int) -> Optional[ExperienceDetail]:
        result = await self.session.execute(select(ExperienceDetailModel).where(ExperienceDetailModel.id == experience_detail_id))
        model = result.scalar_one_or_none()
        if model:
            return ExperienceDetail(
                id=model.id,
                student_id=model.student_id,
                job_offer_id=model.job_offer_id,
                name=model.name,
                description=model.description,
                duration_in_months=model.duration_in_months,
                created_at=model.created_at,
                updated_at=model.updated_at,
                deleted_at=model.deleted_at
            )
        return None

    async def find_by_student_id(self, student_id: int) -> list[ExperienceDetail]:
        result = await self.session.execute(select(ExperienceDetailModel).where(ExperienceDetailModel.student_id == student_id))
        models = result.scalars().all()
        experience_details = []
        for model in models:
            experience_details.append(ExperienceDetail(
                id=model.id,
                student_id=model.student_id,
                job_offer_id=model.job_offer_id,
                name=model.name,
                description=model.description,
                duration_in_months=model.duration_in_months,
                created_at=model.created_at,
                updated_at=model.updated_at,
                deleted_at=model.deleted_at
            ))
        return experience_details

    async def find_by_job_offer_id(self, job_offer_id: int) -> list[ExperienceDetail]:
        result = await self.session.execute(select(ExperienceDetailModel).where(ExperienceDetailModel.job_offer_id == job_offer_id))
        models = result.scalars().all()
        experience_details = []
        for model in models:
            experience_details.append(ExperienceDetail(
                id=model.id,
                student_id=model.student_id,
                job_offer_id=model.job_offer_id,
                name=model.name,
                description=model.description,
                duration_in_months=model.duration_in_months,
                created_at=model.created_at,
                updated_at=model.updated_at,
                deleted_at=model.deleted_at
            ))
        return experience_details

    async def get_all(self) -> list[ExperienceDetail]:
        result = await self.session.execute(select(ExperienceDetailModel))
        models = result.scalars().all()
        experience_details = []
        for model in models:
            experience_details.append(
                ExperienceDetail(
                    id=model.id,
                    student_id=model.student_id,
                    job_offer_id=model.job_offer_id,
                    name=model.name,
                    description=model.description,
                    duration_in_months=model.duration_in_months,
                    created_at=model.created_at,
                    updated_at=model.updated_at,
                    deleted_at=model.deleted_at
                )
            )
        return experience_details

    async def update(self, experience_detail: ExperienceDetail) -> Optional[ExperienceDetail]:
        result = await self.session.execute(select(ExperienceDetailModel).where(ExperienceDetailModel.id == experience_detail.id))
        model = result.scalar_one_or_none()
        if model:
            model.student_id = experience_detail.student_id
            model.job_offer_id = experience_detail.job_offer_id
            model.name = experience_detail.name
            model.description = experience_detail.description
            model.duration_in_months = experience_detail.duration_in_months
            await self.session.commit()
            await self.session.refresh(model)
            return experience_detail
        return None

    async def delete(self, experience_detail_id: int):
        result = await self.session.execute(select(ExperienceDetailModel).where(ExperienceDetailModel.id == experience_detail_id))
        model = result.scalar_one_or_none()
        if not model:
            return False

        await self.session.execute(delete(ExperienceDetailModel).where(ExperienceDetailModel.id == experience_detail_id))
        await self.session.commit()
        return True