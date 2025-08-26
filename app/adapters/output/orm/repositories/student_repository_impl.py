from sqlalchemy.future import select
from sqlalchemy import delete
from typing import Optional

from app.domain.repositories.student_repository import StudentRepository
from app.domain.entities.student import Student
from app.adapters.output.orm.models.student_model import StudentModel
from app.adapters.output.orm.models.student_skill_model import StudentSkillModel
from app.adapters.output.orm.models.student_interest_model import StudentInterestModel
from app.adapters.output.orm.models.experience_detail_model import ExperienceDetailModel
from app.adapters.output.orm.models.interest_model import InterestModel
from app.adapters.output.orm.models.skill_model import SkillModel

class StudentRepositoryImpl(StudentRepository):
    def __init__(self, session):
        self.session = session

    async def get_enriched_students(self, session) -> list:
        students_result = await session.execute(select(StudentModel))
        student_models = students_result.scalars().all()
        enriched_students = []
        for s in student_models:
            experience_detail_links_result = await session.execute(
                select(StudentModel).where(StudentModel.id == s.id))
            experience_detail_links = experience_detail_links_result.scalars().all()
            experience_details = []
            for link in experience_detail_links:
                experience_detail_result = await session.execute(select(ExperienceDetailModel).where(ExperienceDetailModel.id == link.experience_id))
                experience_detail_obj = experience_detail_result.scalar_one_or_none()
                if experience_detail_obj:
                    experience_details.append({"name": experience_detail_obj.name})

            skill_links_result = await session.execute(select(StudentSkillModel).where(StudentSkillModel.student_id == s.id))
            skill_links = skill_links_result.scalars().all()
            skills = []
            for link in skill_links:
                skill_result = await session.execute(select(SkillModel).where(SkillModel.id == link.skill_id))
                skill_obj = skill_result.scalar_one_or_none()
                if skill_obj:
                    skills.append({"name": skill_obj.name})

            interest_links_result = await session.execute(select(StudentInterestModel).where(StudentInterestModel.student_id == s.id))
            interest_links = interest_links_result.scalars().all()
            interests = []
            for link in interest_links:
                interest_result = await session.execute(select(InterestModel).where(InterestModel.id == link.interest_id))
                interest_obj = interest_result.scalar_one_or_none()
                if interest_obj:
                    interests.append({"name": interest_obj.name})
            enriched_students.append({
                "id": s.id,
                "career": s.career,
                "academic_cycle": s.academic_cycle,
                "weekly_availability": s.weekly_availability,
                "preferred_modality": s.preferred_modality,
                "experience_details": experience_details,
                "skills": skills,
                "interests": interests,
                "date_of_birth": s.date_of_birth.isoformat() if s.date_of_birth else None,
                "embedding": s.embedding
            })
        return enriched_students

    async def save(self, student: Student):
        model = StudentModel(
            career=student.career,
            academic_cycle=student.academic_cycle,
            weekly_availability=student.weekly_availability,
            preferred_modality=student.preferred_modality,
            embedding=student.embedding
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def find_by_id(self, student_id: int) -> Optional[Student]:
        result = await self.session.execute(select(StudentModel).where(StudentModel.id == student_id))
        model = result.scalar_one_or_none()
        if model:
            return Student (
                id=model.id,
                career=model.career,
                academic_cycle=model.academic_cycle,
                weekly_availability=model.weekly_availability,
                preferred_modality=model.preferred_modality,
                embedding=model.embedding,
                created_at=model.created_at,
                updated_at=model.updated_at,
                deleted_at=model.deleted_at
            )
        return None

    async def get_all(self) -> list[Student]:
        result = await self.session.execute(select(StudentModel))
        models = result.scalars().all()
        students = []
        for model in models:
            students.append(
                Student (
                    id=model.id,
                    career=model.career,
                    academic_cycle=model.academic_cycle,
                    weekly_availability=model.weekly_availability,
                    preferred_modality=model.preferred_modality,
                    embedding=model.embedding,
                    created_at=model.created_at,
                    updated_at=model.updated_at,
                    deleted_at=model.deleted_at
                )
            )
        return students

    async def update(self, student: Student) -> Optional[Student]:
        result = await self.session.execute(select(StudentModel).where(StudentModel.id == student.id))
        model = result.scalar_one_or_none()
        if model:
            model.career = student.career
            model.academic_cycle = student.academic_cycle
            model.weekly_availability = student.weekly_availability
            model.preferred_modality = student.preferred_modality
            model.embedding = student.embedding
            await self.session.commit()
            await self.session.refresh(model)
            return student
        return None

    async def delete(self, student_id: int) -> bool:
        result = await self.session.execute(select(StudentModel).where(StudentModel.id == student_id))
        model = result.scalar_one_or_none()
        if not model:
            return False

        await self.session.execute(delete(StudentModel).where(StudentModel.id == student_id))
        await self.session.commit()
        return True
