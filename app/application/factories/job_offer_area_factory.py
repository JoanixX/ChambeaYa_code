from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.output.orm.repositories.job_offer_area_repository_impl import JobOfferAreaRepositoryImpl
from app.adapters.output.ports.job_offer_area_port_impl import JobOfferAreaPortImpl
from app.domain.services.job_offer_area_service import JobOfferAreaService
from app.application.use_cases.job_offer_area_use_case import JobOfferAreaUseCase

class JobOfferAreaUseCaseFactory:
    def __init__(self, session: AsyncSession):
        self.session = session

    def build(self) -> JobOfferAreaUseCase:
        port = JobOfferAreaPortImpl(self.session)
        repo = JobOfferAreaRepositoryImpl(self.session)
        service = JobOfferAreaService(repo)
        return JobOfferAreaUseCase(port, service)