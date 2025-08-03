from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.company_use_case import CompanyUseCase
from app.adapters.output.orm.repositories.company_repository_impl import CompanyRepositoryImpl
from app.domain.services.company_service import CompanyService
from app.adapters.output.ports.company_port_impl import CompanyPortImpl

class CompanyUseCaseFactory:
    def __init__(self, session: AsyncSession):
        self.session = session

    def build(self) -> CompanyUseCase:
        company_port = CompanyPortImpl(self.session)
        company_repo = CompanyRepositoryImpl(self.session)
        company_service = CompanyService(company_repo)
        return CompanyUseCase(company_port, company_service)