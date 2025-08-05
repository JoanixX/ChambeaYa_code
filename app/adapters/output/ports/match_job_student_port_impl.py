from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.match_job_student import MatchJobStudent
from app.adapters.output.orm.repositories.match_job_student_repository_impl import MatchJobStudentRepositoryImpl
from app.application.ports.match_job_student_port import MatchJobStudentPort

from app.domain.services.match_job_student_service import MatchJobStudentService
from app.adapters.output.orm.repositories.match_job_student_repository_impl import MatchJobStudentRepositoryImpl

class MatchJobStudentPortImpl(MatchJobStudentPort):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.match_job_student_repo = MatchJobStudentRepositoryImpl(session)
        self.service = MatchJobStudentService(self.match_job_student_repo, self, session)

    async def match_job_student(self, student, job_offers):
        return await self.service.match_best_from_student(student, job_offers)

    async def match_student_job(self, job_offer, students):
        return await self.service.match_best_from_offer(job_offer, students)