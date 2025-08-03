from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.output.orm.repositories.student_interest_repository_impl import StudentInterestRepositoryImpl
from app.adapters.output.ports.student_interest_port_impl import StudentInterestPortImpl
from app.domain.services.student_interest_service import StudentInterestService
from app.application.use_cases.student_interest_use_case import StudentInterestUseCase

class StudentInterestUseCaseFactory:
    def __init__(self, session: AsyncSession):
        self.session = session

    def build(self) -> StudentInterestUseCase:
        port = StudentInterestPortImpl(self.session)
        repo = StudentInterestRepositoryImpl(self.session)
        service = StudentInterestService(repo)
        return StudentInterestUseCase(port, service)