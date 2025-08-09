from sqlalchemy.future import select
from typing import Optional

from app.domain.repositories.filter_match_repository import FilterMatchRepository
from app.domain.entities.filter_match import FilterMatch
from app.adapters.output.orm.models.filter_match_model import FilterMatchModel

class FilterMatchRepositoryImpl(FilterMatchRepository):
    def __init__(self, session):
        self.session = session
    
    async def preprocess_all_job_offers(self, job_offer_ids: list[int]) -> list[FilterMatch]:
        results = []
        for job_offer_id in job_offer_ids:
            result = await self.preprocess_job_offer(job_offer_id)
            if result:
                results.append(result)
        return results

    async def preprocess_job_offer(self, job_offer_id: int) -> Optional[FilterMatch]:
        result = await self.session.execute(
            select(FilterMatchModel).where(FilterMatchModel.job_offer_id == job_offer_id)
        )
        row = result.scalar_one_or_none()
        if row:
            return FilterMatch(
                id=row.id,
                job_offer_id=row.job_offer_id,
                student_id=row.student_id,
                status=row.status,
                stage=row.stage,
                created_at=row.created_at,
                updated_at=row.updated_at
            )
        return None
    
    async def preprocess_all_students(self, student_ids: list[int]) -> list[FilterMatch]:
        results = []
        for student_id in student_ids:
            result = await self.preprocess_student(student_id)
            if result:
                results.append(result)
        return results
    
    async def preprocess_student(self, student_id: int) -> Optional[FilterMatch]:
        result = await self.session.execute(
            select(FilterMatchModel).where(FilterMatchModel.student_id == student_id)
        )
        row = result.scalar_one_or_none()
        if row:
            return FilterMatch(
                id=row.id,
                job_offer_id=row.job_offer_id,
                student_id=row.student_id,
                status=row.status,
                stage=row.stage,
                created_at=row.created_at,
                updated_at=row.updated_at
            )
        return None
    
    async def save_filtered_student(self, filter_match: FilterMatch) -> FilterMatchModel:
        model = FilterMatchModel(
            student_id=filter_match.student_id,
            job_offer_id=None,
            stage=filter_match.stage,
            status=filter_match.status
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def save_filtered_job_offer(self, filter_match: FilterMatch) -> FilterMatchModel:
        model = FilterMatchModel(
            job_offer_id=filter_match.job_offer_id,
            student_id=None,
            stage=filter_match.stage,
            status=filter_match.status
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model