from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.output.orm.repositories.company_area_repository_impl import CompanyAreaRepositoryImpl
from app.adapters.output.ports.company_area_port_impl import CompanyAreaPortImpl
from app.domain.services.company_area_service import CompanyAreaService
from app.application.use_cases.company_area_use_case import CompanyAreaUseCase

class CompanyAreaUseCaseFactory:
    def __init__(self, session: AsyncSession):
        self.session = session

    def build(self) -> CompanyAreaUseCase:
        port = CompanyAreaPortImpl(self.session)
        repo = CompanyAreaRepositoryImpl(self.session)
        service = CompanyAreaService(repo)
        return CompanyAreaUseCase(port, service)