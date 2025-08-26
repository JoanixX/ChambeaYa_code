from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.external_link_use_case import ExternalLinkUseCase
from app.adapters.output.orm.repositories.external_link_repository_impl import ExternalLinkRepositoryImpl
from app.domain.services.external_link_service import ExternalLinkService
from app.adapters.output.ports.external_link_port_impl import ExternalLinkPortImpl

class ExternalLinkUseCaseFactory:
    def __init__(self, session: AsyncSession):
        self.session = session

    def build(self) -> ExternalLinkUseCase:
        external_link_port = ExternalLinkPortImpl(self.session)
        external_link_repo = ExternalLinkRepositoryImpl(self.session)
        external_link_service = ExternalLinkService(external_link_repo)
        return ExternalLinkUseCase(external_link_port, external_link_service)