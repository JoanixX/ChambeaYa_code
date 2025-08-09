from sqlalchemy.future import select
from typing import Optional

from app.domain.repositories.match_job_student_repository import MatchJobStudentRepository
from app.domain.entities.match_job_student import MatchJobStudent
from app.adapters.output.orm.models.match_job_student_model import MatchJobStudentModel

class MatchJobStudentRepositoryImpl(MatchJobStudentRepository):
    def __init__(self, session):
        self.session = session

    async def save(self, filter_match: MatchJobStudent) -> MatchJobStudent:
        model = MatchJobStudentModel(
            match_job_student_id=filter_match.id,
            student_id = filter_match.student_id,
            job_offer_id=filter_match.job_offer_id,
            score=filter_match.score,
            match_date=filter_match.match_date,
            rank=filter_match.rank
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def match_best_from_student(self, student_id: int) -> Optional[MatchJobStudent]:
        result = await self.session.execute(
            select(MatchJobStudentModel).where(MatchJobStudentModel.student_id == student_id)
        )
        row = result.scalar_one_or_none()
        if row:
            return MatchJobStudent(
                id=row.match_job_student_id,
                student_id=row.student_id,
                job_offer_id=row.job_offer_id,
                score=row.score,
                match_date=row.match_date,
                rank=row.rank
            )
        return None

    async def match_best_from_job_offer(self, job_offer_id: int) -> Optional[MatchJobStudent]:
        result = await self.session.execute(
            select(MatchJobStudentModel).where(MatchJobStudentModel.job_offer_id == job_offer_id)
        )
        row = result.scalar_one_or_none()
        if row:
            return MatchJobStudent(
                id=row.match_job_student_id,
                student_id=row.student_id,
                job_offer_id=row.job_offer_id,
                score=row.score,
                match_date=row.match_date,
                rank=row.rank
            )
        return None