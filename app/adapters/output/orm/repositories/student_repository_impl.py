from app.domain.repositories.student_repository import StudentRepository
from app.domain.entities.student import Student
from app.adapters.output.orm.models.student_model import StudentModel
from sqlalchemy.future import select
from sqlalchemy import delete
from typing import Optional
from app.domain.repositories.student_repository import StudentRepository

class StudentRepositoryImpl(StudentRepository):
    def __init__(self, session):
        self.session = session

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

    async def update(self, student: Student):
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

    async def delete(self, student_id: int):
        await self.session.execute(delete(StudentModel).where(StudentModel.id == student_id))
        await self.session.commit()
