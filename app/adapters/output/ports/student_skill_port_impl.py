from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.student_skill import StudentSkill
from app.adapters.output.orm.repositories.student_skill_repository_impl import StudentSkillRepositoryImpl
from app.application.ports.student_skill_port import StudentSkillPort

class StudentSkillPortImpl(StudentSkillPort):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.student_skill_repo = StudentSkillRepositoryImpl(session)

    async def add_student_skill(self, student_skill: StudentSkill) -> StudentSkill:
        return await self.student_skill_repo.save(student_skill)

    async def get_student_skills(self, student_id: int) -> List[StudentSkill]:
        return await self.student_skill_repo.get_by_student_id(student_id)
    
    async def delete_student_skill(self, student_id: int, skill_id: int) -> bool:
        return await self.student_skill_repo.delete(student_id, skill_id)
    
    async def student_skill_exists(self, student_id: int, skill_id: int) -> bool:
        return await self.student_skill_repo.exists(student_id, skill_id)