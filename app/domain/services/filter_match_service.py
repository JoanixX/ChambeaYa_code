import logging
from typing import Any, Optional, List, Dict
from datetime import datetime

from app.domain.repositories.filter_match_repository import FilterMatchRepository
from app.domain.entities.filter_match import FilterMatch
from app.adapters.output.orm.repositories.job_offer_repository_impl import JobOfferRepositoryImpl
from app.adapters.output.orm.repositories.student_repository_impl import StudentRepositoryImpl

class FilterMatchService:
    def __init__(self, filter_match_repo: FilterMatchRepository, session):
        self.filter_match_repo = filter_match_repo
        self.session = session
        self.job_offer_repo = JobOfferRepositoryImpl(session)
        self.student_repo = StudentRepositoryImpl(session)

    async def preprocess_all_job_offers(self, job_offer_ids: List[int]) -> List[dict]:
        logging.info(f"[BACKEND] preprocess_all_job_offers received job_offer_ids: {job_offer_ids}")
        result = await self.filter_match_repo.preprocess_all_job_offers(job_offer_ids)
        logging.info(f"[BACKEND] preprocess_all_job_offers sending to IA repo: {result}")
        return result

    async def preprocess_job_offer(self, job_offer_id: int) -> Optional[dict]:
        logging.info(f"[BACKEND] preprocess_job_offer received job_offer_id: {job_offer_id}")
        result = await self.filter_match_repo.preprocess_job_offer(job_offer_id)
        logging.info(f"[BACKEND] preprocess_job_offer sending to IA repo: {result}")
        return result

    async def preprocess_all_students(self, students_ids: List[int]) -> List[dict]:
        logging.info(f"[BACKEND] preprocess_all_students received students_ids: {students_ids}")
        result = await self.filter_match_repo.preprocess_all_students(students_ids)
        logging.info(f"[BACKEND] preprocess_all_students sending to IA repo: {result}")
        return result

    async def preprocess_student(self, student_id: int) -> Optional[dict]:
        logging.info(f"[BACKEND] preprocess_student received student_id: {student_id}")
        result = await self.filter_match_repo.preprocess_student(student_id)
        logging.info(f"[BACKEND] preprocess_student sending to IA repo: {result}")
        return result

    async def save_filtered_student(self, student_id: int, filter_match_data: Dict[str, Any]) -> int:
        filter_match = self.filter_match_entity(filter_match_data, student_id)
        saved_model = await self.filter_match_repo.save_filtered_student(filter_match)
        if saved_model:
            return saved_model.id
        else:
            raise ValueError("Error al guardar el filtrado del estudiante")

    async def save_filtered_job_offer(self, job_offer_id: int, filter_match_data: Dict[str, Any]) -> int:
        filter_match = self.filter_match_entity(filter_match_data, job_offer_id)
        saved_model = await self.filter_match_repo.save_filtered_job_offer(filter_match)
        if saved_model:
            return saved_model.id
        else:
            raise ValueError("Error al guardar el filtrado de la oferta de trabajo")

    def filter_match_entity(
        self,
        filter_match_data: Dict[str, Any],
        student_id: Optional[int] = None,
        job_offer_id: Optional[int] = None
    ) -> FilterMatch:
        if 'created_at' not in filter_match_data:
            filter_match_data['created_at'] = datetime.now()
        if 'updated_at' not in filter_match_data:
            filter_match_data['updated_at'] = datetime.now()
        return FilterMatch(
            id=0,
            job_offer_id=job_offer_id,
            student_id=student_id,
            status=filter_match_data.get("status", None),
            stage=filter_match_data.get("stage", None),
            created_at=filter_match_data['created_at'],
            updated_at=filter_match_data['updated_at']
        )
