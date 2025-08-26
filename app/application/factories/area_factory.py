from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.area_use_case import AreaUseCase
from app.adapters.output.orm.repositories.area_repository_impl import AreaRepositoryImpl
from app.domain.services.area_service import AreaService
from app.adapters.output.ports.area_port_impl import AreaPortImpl

class AreaUseCaseFactory:
    def __init__(self, session: AsyncSession):
        self.session = session

    def build(self) -> AreaUseCase:
        area_port = AreaPortImpl(self.session)
        area_repo = AreaRepositoryImpl(self.session)
        area_service = AreaService(area_repo)
        return AreaUseCase(area_port, area_service)