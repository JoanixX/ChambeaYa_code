from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.interest_use_case import InterestUseCase
from app.adapters.output.orm.repositories.interest_repository_impl import InterestRepositoryImpl
from app.domain.services.interest_service import InterestService
from app.adapters.output.ports.interest_port_impl import InterestPortImpl

class InterestUseCaseFactory:
    def __init__(self, session: AsyncSession):
        self.session = session

    def build(self) -> InterestUseCase:
        interest_port = InterestPortImpl(self.session)
        interest_repo = InterestRepositoryImpl(self.session)
        interest_service = InterestService(interest_repo)
        return InterestUseCase(interest_port, interest_service)