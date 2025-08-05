from sqlalchemy.ext.asyncio import AsyncSession
from app.application.use_cases.match_job_student_use_case import MatchJobStudentUseCase
from app.adapters.output.ports.match_job_student_port_impl import MatchJobStudentPortImpl

class MatchJobStudentUseCaseFactory:
    @staticmethod
    def create(session: AsyncSession) -> MatchJobStudentUseCase:
        match_job_student_port = MatchJobStudentPortImpl(session)
        return MatchJobStudentUseCase(match_job_student_port)