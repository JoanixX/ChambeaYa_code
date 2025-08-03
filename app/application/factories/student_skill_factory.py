from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.output.orm.repositories.student_skill_repository_impl import StudentSkillRepositoryImpl
from app.adapters.output.ports.student_skill_port_impl import StudentSkillPortImpl
from app.domain.services.student_skill_service import StudentSkillService
from app.application.use_cases.student_skill_use_case import StudentSkillUseCase

class StudentSkillUseCaseFactory:
    def __init__(self, session: AsyncSession):
        self.session = session

    def build(self) -> StudentSkillUseCase:
        port = StudentSkillPortImpl(self.session)
        repo = StudentSkillRepositoryImpl(self.session)
        service = StudentSkillService(repo)
        return StudentSkillUseCase(port, service)