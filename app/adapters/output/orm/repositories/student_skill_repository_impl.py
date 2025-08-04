from typing import List
from sqlalchemy.future import select
from sqlalchemy import delete
from app.domain.entities.student_skill import StudentSkill
from app.domain.repositories.student_skill_repository import StudentSkillRepository
from app.adapters.output.orm.models.student_skill_model import StudentSkillModel

class StudentSkillRepositoryImpl(StudentSkillRepository):
    def __init__(self, session):
        self.session = session

    async def get_by_student_id(self, student_id: int) -> List[StudentSkill]:
        result = await self.session.execute(
            select(StudentSkillModel).where(StudentSkillModel.student_id == student_id)
        )
        models = result.scalars().all()
        skills = []
        for model in models:
            skills.append(
                StudentSkill(
                    student_id=model.student_id, 
                    skill_id=model.skill_id
                )
            )
        return skills

    async def exists(self, student_id: int, skill_id: int) -> bool:
        result = await self.session.execute(
            select(StudentSkillModel).where(
                StudentSkillModel.student_id == student_id,
                StudentSkillModel.skill_id == skill_id
            )
        )
        return result.scalar_one_or_none() is not None

    async def save(self, student_skill: StudentSkill) -> StudentSkill:
        exists = await self.exists(student_skill.student_id, student_skill.skill_id)
        if exists:
            return student_skill
        
        model = StudentSkillModel(
            student_id=student_skill.student_id,
            skill_id=student_skill.skill_id
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return StudentSkill(student_id=model.student_id, skill_id=model.skill_id)

    async def delete(self, student_id: int, skill_id: int) -> bool:
        result = await self.session.execute(
            select(StudentSkillModel).where(
                StudentSkillModel.student_id == student_id,
                StudentSkillModel.skill_id == skill_id
            )
        )
        model = result.scalar_one_or_none()
        if not model:
            return False

        await self.session.execute(
            delete(StudentSkillModel).where(
                StudentSkillModel.student_id == student_id,
                StudentSkillModel.skill_id == skill_id
            )
        )
        await self.session.commit()
        return True