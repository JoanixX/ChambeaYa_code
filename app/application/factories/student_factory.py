from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.student_use_case import StudentUseCase
from app.adapters.output.orm.repositories.student_repository_impl import StudentRepositoryImpl
from app.domain.services.student_service import StudentService
from app.adapters.output.ports.student_port_impl import StudentPortImpl

class StudentUseCaseFactory:
    def __init__(self, session: AsyncSession):
        self.session = session

    def build(self) -> StudentUseCase:
        student_port = StudentPortImpl(self.session)
        student_repo = StudentRepositoryImpl(self.session)
        student_service = StudentService(student_repo)
        return StudentUseCase(student_port, student_service)