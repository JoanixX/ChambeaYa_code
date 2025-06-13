from app.application.ports.register_student_port import RegisterStudentPort
from app.domain.entities.student import Student
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

class RegisterStudentUseCase(RegisterStudentPort):
    async def register(self, *, name: str, email: str, date_of_birth, enrollment_date, session: AsyncSession):
        if enrollment_date.tzinfo is not None:
            enrollment_date = enrollment_date.replace(tzinfo=None)
        new_student = Student(
            name=name,
            email=email,
            date_of_birth=date_of_birth,
            enrollment_date=enrollment_date
        )
        session.add(new_student)
        await session.commit()
        await session.refresh(new_student)
        return new_student
