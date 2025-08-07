from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.domain.entities.filter_match import FilterMatch
from app.adapters.output.orm.repositories.filter_match_repository_impl import FilterMatchRepositoryImpl
from app.application.ports.filter_match_port import FilterMatchPort

class FilterMatchPortImpl(FilterMatchPort):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.filter_match_repo = FilterMatchRepositoryImpl(session)

    async def preprocess_all_job_offers(self, job_offer_ids: List[int]) -> List[dict]:
        dicts = await self.filter_match_repo.preprocess_all_job_offers(job_offer_ids)
        for d in dicts:
            if isinstance(d, FilterMatch):
                if not hasattr(d, 'created_at') or d.created_at is None:
                    d.created_at = datetime.utcnow()
                d.updated_at = datetime.utcnow()
        return [self._to_response_dict(d) for d in dicts if d is not None]

    async def preprocess_job_offer(self, job_offer_id: int) -> dict:
        d = await self.filter_match_repo.preprocess_job_offer(job_offer_id)
        if isinstance(d, FilterMatch):
            if not hasattr(d, 'created_at') or d.created_at is None:
                d.created_at = datetime.utcnow()
            d.updated_at = datetime.utcnow()
        if d:
            return self._to_response_dict(d)
        nuevo = {"job_offer_id": job_offer_id, "status": "pending", "stage": 0, "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()}
        return nuevo

    async def preprocess_all_students(self, student_ids: List[int]) -> List[dict]:
        dicts = await self.filter_match_repo.preprocess_all_students(student_ids)
        for d in dicts:
            if isinstance(d, FilterMatch):
                if not hasattr(d, 'created_at') or d.created_at is None:
                    d.created_at = datetime.utcnow()
                d.updated_at = datetime.utcnow()
        return [self._to_response_dict(d) for d in dicts if d is not None]

    async def preprocess_student(self, student_id: int) -> dict:
        d = await self.filter_match_repo.preprocess_student(student_id)
        if isinstance(d, FilterMatch):
            if not hasattr(d, 'created_at') or d.created_at is None:
                d.created_at = datetime.utcnow()
            d.updated_at = datetime.utcnow()
        if d:
            return self._to_response_dict(d)
        nuevo = {"student_id": student_id, "status": "pending", "stage": 0, "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()}
        return nuevo

    def _to_response_dict(self, data):
        if data is None:
            return {}
        if isinstance(data, dict):
            return data
        return {
            "job_offer_id": getattr(data, "job_offer_id", None),
            "student_id": getattr(data, "student_id", None),
            "status": getattr(data, "status", None),
            "stage": getattr(data, "stage", None)
        }