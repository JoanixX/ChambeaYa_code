from app.application.ports.register_student_port import RegisterStudentPort
from app.domain.entities.student import Student
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

class RegisterStudentUseCase(RegisterStudentPort):
    async def register(
        self,
        *,
        name: str,
        email: str,
        date_of_birth,
        experience_id: int,
        location: str,
        weekly_availability: int,
        preferred_modality: int,
        career: str,
        academic_cycle: int,
        main_motivation: str,
        description: str,
        session: AsyncSession
    ):
        new_student = Student(
            name=name,
            email=email,
            date_of_birth=date_of_birth,
            experience_id=experience_id,
            location=location,
            weekly_availability=weekly_availability,
            preferred_modality=preferred_modality,
            career=career,
            academic_cycle=academic_cycle,
            main_motivation=main_motivation,
            description=description
        )
        session.add(new_student)
        await session.commit()
        await session.refresh(new_student)
        return new_student
