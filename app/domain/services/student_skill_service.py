from app.domain.entities.student_skill import StudentSkill
from app.domain.repositories.student_skill_repository import StudentSkillRepository
from typing import List

class StudentSkillService:
    def __init__(self, student_skill_repo: StudentSkillRepository):
        self.student_skill_repo = student_skill_repo

    async def add_student_skill(self, student_skill: StudentSkill) -> StudentSkill:
        exists = await self.student_skill_repo.exists(student_skill.student_id, student_skill.skill_id)

        if exists:
            raise ValueError("El estudiante ya tiene esta habilidad asignada")

        saved_model = await self.student_skill_repo.save(student_skill)

        if saved_model:
            return saved_model
        else:
            raise ValueError("Error al guardar la habilidad del estudiante")

    async def get_student_skills(self, student_id: int) -> List[StudentSkill]:
        return await self.student_skill_repo.get_by_student_id(student_id)

    async def delete_student_skill(self, student_id: int, skill_id: int) -> bool:
        return await self.student_skill_repo.delete(student_id, skill_id)
