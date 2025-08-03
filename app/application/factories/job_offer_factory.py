from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.job_offer_use_case import JobOfferUseCase
from app.adapters.output.orm.repositories.job_offer_repository_impl import JobOfferRepositoryImpl
from app.domain.services.job_offer_service import JobOfferService
from app.adapters.output.ports.job_offer_port_impl import JobOfferPortImpl

class JobOfferUseCaseFactory:
    def __init__(self, session: AsyncSession):
        self.session = session

    def build(self) -> JobOfferUseCase:
        job_offer_port = JobOfferPortImpl(self.session)
        job_offer_repo = JobOfferRepositoryImpl(self.session)
        job_offer_service = JobOfferService(job_offer_repo)
        return JobOfferUseCase(job_offer_port, job_offer_service)