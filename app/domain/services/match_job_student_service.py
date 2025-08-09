import logging
from typing import Any, List, Dict
from datetime import datetime

from app.domain.repositories.match_job_student_repository import MatchJobStudentRepository
from app.domain.entities.match_job_student import MatchJobStudent
from app.domain.entities.job_offer import JobOffer
from app.domain.entities.student import Student

class MatchJobStudentService:
    def __init__(self, match_js_repo: MatchJobStudentRepository, session):
        self.match_js_repo = match_js_repo
        self.session = session

    async def match_best_from_student(self, student: Student, job_offers: List[JobOffer]):
        return await self.match_js_repo.match_best_from_student(student, job_offers)

    async def match_best_from_job_offer(self, job_offer: JobOffer, students: List[Student]):
        return await self.match_js_repo.match_best_from_job_offer(job_offer, students)

    async def register_match_job_student(self, match_data: Dict[str, Any], job_offer_id: int, student_id: int) -> int:
        match_job_student = self.match_job_student_entity(match_data, job_offer_id, student_id)
        saved_model = await self.match_js_repo.save(match_job_student)
        if saved_model:
            return saved_model.id
        else:
            raise ValueError("Error al guardar el match")
    
    def match_job_student_entity(
        self,
        match_data: Dict[str, Any],
        job_offer_id: int,
        student_id: int
    ) -> MatchJobStudent:
        if 'match_date' not in match_data:
            match_data['match_date'] = datetime.now()
        if 'updated_at' not in match_data:
            match_data['updated_at'] = datetime.now()
        return MatchJobStudent(
            id=0,
            job_offer_id=job_offer_id,
            student_id=student_id,
            score=match_data.get('score', None),
            match_date=match_data['match_date'],
            rank= match_data.get('rank', None),
            updated_at=match_data['updated_at'],
        )