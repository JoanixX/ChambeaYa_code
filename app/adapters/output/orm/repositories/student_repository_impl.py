from app.domain.repositories.student_repository import StudentRepository
from app.domain.entities.student import Student
from app.adapters.output.orm.models.student_model import StudentModel
from sqlalchemy.future import select
from sqlalchemy import delete
from typing import Optional


# Mapper ORM -> Entidad de dominio
def student_model_to_entity(model: StudentModel) -> Student:
    return Student(
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

async def get_all_students_impl(session):
    result = await session.execute(select(StudentModel))
    models = result.scalars().all()
    return [student_model_to_entity(m) for m in models]

async def get_student_by_id_impl(session, student_id: int):
    result = await session.execute(select(StudentModel).where(StudentModel.id == student_id))
    model = result.scalar_one_or_none()
    return student_model_to_entity(model) if model else None

async def get_student_by_email_impl(session, email: str):
    result = await session.execute(select(StudentModel).where(StudentModel.email == email))
    model = result.scalar_one_or_none()
    return student_model_to_entity(model) if model else None

async def save_student_impl(session, student: Student):
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
    session.add(model)
    await session.commit()
    await session.refresh(model)
    return model

async def update_student_impl(session, student: Student):
    result = await session.execute(select(StudentModel).where(StudentModel.id == student.id))
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
        await session.commit()
        await session.refresh(model)

async def delete_student_impl(session, student_id: int):
    await session.execute(delete(StudentModel).where(StudentModel.id == student_id))
    await session.commit()
