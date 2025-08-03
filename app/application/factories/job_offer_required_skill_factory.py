from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.output.orm.repositories.job_offer_required_skill_repository_impl import JobOfferRequiredSkillRepositoryImpl
from app.adapters.output.ports.job_offer_required_skill_port_impl import JobOfferRequiredSkillPortImpl
from app.domain.services.job_offer_required_skill_service import JobOfferRequiredSkillService
from app.application.use_cases.job_offer_required_skill_use_case import JobOfferRequiredSkillUseCase

class JobOfferRequiredSkillUseCaseFactory:
    def __init__(self, session: AsyncSession):
        self.session = session

    def build(self) -> JobOfferRequiredSkillUseCase:
        port = JobOfferRequiredSkillPortImpl(self.session)
        repo = JobOfferRequiredSkillRepositoryImpl(self.session)
        service = JobOfferRequiredSkillService(repo)
        return JobOfferRequiredSkillUseCase(port, service)