from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.experience_detail_use_case import ExperienceDetailUseCase
from app.adapters.output.orm.repositories.experience_detail_repository_impl import ExperienceDetailRepositoryImpl
from app.domain.services.experience_detail_service import ExperienceDetailService
from app.adapters.output.ports.experience_detail_port_impl import ExperienceDetailPortImpl

class ExperienceDetailUseCaseFactory:
    def __init__(self, session: AsyncSession):
        self.session = session

    def build(self) -> ExperienceDetailUseCase:
        experience_detail_port = ExperienceDetailPortImpl(self.session)
        experience_detail_repo = ExperienceDetailRepositoryImpl(self.session)
        experience_detail_service = ExperienceDetailService(experience_detail_repo)
        return ExperienceDetailUseCase(experience_detail_port, experience_detail_service)