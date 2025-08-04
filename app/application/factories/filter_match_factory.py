from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.filter_match_use_case import FilterMatchUseCase
from app.adapters.output.orm.repositories.filter_match_repository_impl import FilterMatchRepositoryImpl
from app.domain.services.filter_match_service import FilterMatchService
from app.adapters.output.ports.filter_match_port_impl import FilterMatchPortImpl

class FilterMatchUseCaseFactory:
    @staticmethod
    def create(session: AsyncSession) -> FilterMatchUseCase:
        filter_match_repo = FilterMatchRepositoryImpl(session)
        filter_match_port = FilterMatchPortImpl(session)
        filter_match_service = FilterMatchService(filter_match_repo, session)
        return FilterMatchUseCase(filter_match_port, filter_match_service)