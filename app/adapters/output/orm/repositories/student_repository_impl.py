from app.domain.repositories.student_repository import StudentRepository
from app.domain.entities.student import Student
from app.adapters.output.orm.models.student_model import StudentModel
from sqlalchemy.future import select
from sqlalchemy import delete
from typing import Optional
from app.adapters.output.orm.models.student_skill_model import StudentSkillModel
from app.adapters.output.orm.models.student_interest_model import StudentInterestModel
from app.adapters.output.orm.repositories.experience_detail_repository_impl import get_experience_name_by_id_impl
from app.adapters.output.orm.models.interest_model import InterestModel

class StudentRepositoryImpl(StudentRepository):
    def __init__(self, session):
        self.session = session

    async def get_enriched_students(self, session) -> list:
        students_result = await session.execute(select(StudentModel))
        student_models = students_result.scalars().all()
        enriched_students = []
        for s in student_models:
            experience_name = None
            if s.experience_id:
                experience_name = await get_experience_name_by_id_impl(session, s.experience_id)

            skill_links_result = await session.execute(select(StudentSkillModel).where(StudentSkillModel.student_id == s.id))
            skill_links = skill_links_result.scalars().all()
            skills = []
            for link in skill_links:
                skill = await get_skill_by_id_impl(session, link.skill_id)
                if skill:
                    skills.append({"name": skill.name})

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
                "name": s.name,
                "email": s.email,
                "career": s.career,
                "academic_cycle": s.academic_cycle,
                "location": s.location,
                "main_motivation": s.main_motivation,
                "description": s.description,
                "weekly_availability": s.weekly_availability,
                "preferred_modality": s.preferred_modality,
                "experience": experience_name,
                "experience_id": s.experience_id,
                "skills": skills,
                "interests": interests,
                "date_of_birth": s.date_of_birth.isoformat() if s.date_of_birth else None,
                "embedding": s.embedding
            })
        return enriched_students

    async def save(self, student: Student):
        model = StudentModel(
            name=student.name,
            email=student.email,
            career=student.career,
            academic_cycle=student.academic_cycle,
            location=student.location,
            main_motivation=student.main_motivation,
            description=student.description,
            weekly_availability=student.weekly_availability,
            preferred_modality=student.preferred_modality,
            experience_id=student.experience_id,
            date_of_birth=student.date_of_birth,
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
                name=model.name,
                email=model.email,
                career=model.career,
                academic_cycle=model.academic_cycle,
                location=model.location,
                main_motivation=model.main_motivation,
                description=model.description,
                weekly_availability=model.weekly_availability,
                preferred_modality=model.preferred_modality,
                experience_id=model.experience_id,
                date_of_birth=model.date_of_birth,
                embedding=model.embedding
            )
        return None

    async def find_by_email(self, email: str) -> Optional[Student]:
        result = await self.session.execute(select(StudentModel).where(StudentModel.email == email))
        model = result.scalar_one_or_none()
        if model:
            return Student (
                id=model.id,
                name=model.name,
                email=model.email,
                career=model.career,
                academic_cycle=model.academic_cycle,
                location=model.location,
                main_motivation=model.main_motivation,
                description=model.description,
                weekly_availability=model.weekly_availability,
                preferred_modality=model.preferred_modality,
                experience_id=model.experience_id,
                date_of_birth=model.date_of_birth,
                embedding=model.embedding
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
                name=model.name,
                email=model.email,
                career=model.career,
                academic_cycle=model.academic_cycle,
                location=model.location,
                main_motivation=model.main_motivation,
                description=model.description,
                weekly_availability=model.weekly_availability,
                preferred_modality=model.preferred_modality,
                experience_id=model.experience_id,
                date_of_birth=model.date_of_birth,
                embedding=model.embedding
                )
            )
        return students

    async def update(self, student: Student) -> Optional[Student]:
        result = await self.session.execute(select(StudentModel).where(StudentModel.id == student.id))
        model = result.scalar_one_or_none()
        if model:
            model.name = student.name
            model.email = student.email
            model.career = student.career
            model.academic_cycle = student.academic_cycle
            model.location = student.location
            model.main_motivation = student.main_motivation
            model.description = student.description
            model.weekly_availability = student.weekly_availability
            model.preferred_modality = student.preferred_modality
            model.experience_id = student.experience_id
            model.date_of_birth = student.date_of_birth
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
