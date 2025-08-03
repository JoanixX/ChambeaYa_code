from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.skill_use_case import SkillUseCase
from app.adapters.output.orm.repositories.skill_repository_impl import SkillRepositoryImpl
from app.domain.services.skill_service import SkillService
from app.adapters.output.ports.skill_port_impl import SkillPortImpl

class SkillUseCaseFactory:
    def __init__(self, session: AsyncSession):
        self.session = session

    def build(self) -> SkillUseCase:
        skill_port = SkillPortImpl(self.session)
        skill_repo = SkillRepositoryImpl(self.session)
        skill_service = SkillService(skill_repo)
        return SkillUseCase(skill_port, skill_service)