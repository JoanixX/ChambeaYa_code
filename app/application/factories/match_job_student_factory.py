from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.match_job_student_use_case import MatchJobStudentUseCase
from app.adapters.output.ports.match_job_student_port_impl import MatchJobStudentPortImpl
from app.adapters.output.orm.repositories.match_job_student_repository_impl import MatchJobStudentRepositoryImpl
from app.domain.services.match_job_student_service import MatchJobStudentService

class MatchJobStudentUseCaseFactory:
    def __init__(self, session: AsyncSession):
        self.session = session

    def build(self) -> MatchJobStudentUseCase:
        filter_match_repo = MatchJobStudentRepositoryImpl(self.session)
        filter_match_port = MatchJobStudentPortImpl(self.session)
        filter_match_service = MatchJobStudentService(filter_match_repo, self.session)
        return MatchJobStudentUseCase(filter_match_port, filter_match_service)