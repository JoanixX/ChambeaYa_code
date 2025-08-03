from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.agreement_use_case import AgreementUseCase
from app.adapters.output.orm.repositories.agreement_repository_impl import AgreementRepositoryImpl
from app.domain.services.agreement_service import AgreementService
from app.adapters.output.ports.agreement_port_impl import AgreementPortImpl

class AgreementUseCaseFactory:
    def __init__(self, session: AsyncSession):
        self.session = session

    def build(self) -> AgreementUseCase:
        agreement_port = AgreementPortImpl(self.session)
        agreement_repo = AgreementRepositoryImpl(self.session)
        agreement_service = AgreementService(agreement_repo)
        return AgreementUseCase(agreement_port, agreement_service)