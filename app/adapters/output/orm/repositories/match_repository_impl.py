from app.domain.repositories.match_job_student_repository import MatchJobStudentRepository
from app.domain.entities.match_job_student import MatchJobStudent
from app.adapters.output.orm.models.match_job_student_model import MatchJobStudentModel

class MatchJobStudentRepositoryImpl(MatchJobStudentRepository):
    def __init__(self, session):
        self.session = session

    async def save(self, filter_match: MatchJobStudent):
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

    async def match_job_student(self, student_id: int, job_offer_id: int) -> MatchJobStudent:
        model = await self.session.get(MatchJobStudentModel, (student_id, job_offer_id))
        if model:
            return MatchJobStudent(
                match_job_student_id=model.id,
                student_id = model.student_id,
                job_offer_id=model.job_offer_id,
                score=model.score,
                match_date=model.match_date,
                rank=model.rank
            )
        return None