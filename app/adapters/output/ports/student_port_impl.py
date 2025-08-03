from typing import Dict, Any, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.adapters.output.orm.repositories.student_repository_impl import StudentRepositoryImpl
from app.application.ports.student_port import StudentPort
from app.domain.entities.student import Student

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StudentPortImpl(StudentPort):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.student_repo = StudentRepositoryImpl(session)

    async def register_student(self, student_data: Dict[str, Any]) -> Student:
        student = Student(
            id=0,
            name=student_data["name"],
            email=student_data["email"],
            career=student_data["career"],
            academic_cycle=student_data["academic_cycle"],
            location=student_data["location"],
            main_motivation=student_data["main_motivation"],
            description=student_data["description"],
            weekly_availability=student_data["weekly_availability"],
            preferred_modality=student_data["preferred_modality"],
            experience_id=student_data.get("experience_id", None),
            date_of_birth=student_data["date_of_birth"],
            embedding={}
        )

        saved_student = await self.student_repo.save(student)
        return saved_student

    async def get_student(self, student_id: int) -> Optional[Student]:
        return await self.student_repo.find_by_id(student_id)

    async def get_all_students(self) -> List[Student]:
        return await self.student_repo.get_all()

    async def update_student(self, student_id: int, student_data: Dict[str, Any]) -> Optional[Student]:
        existing_student = await self.student_repo.find_by_id(student_id)
        if not existing_student:
            return None

        updated_student = Student(
            id=student_id,
            name=student_data.get("name", existing_student.name),
            email=student_data.get("email", existing_student.email),
            career=student_data.get("career", existing_student.career),
            academic_cycle=student_data.get("academic_cycle", existing_student.academic_cycle),
            location=student_data.get("location", existing_student.location),
            main_motivation=student_data.get("main_motivation", existing_student.main_motivation),
            description=student_data.get("description", existing_student.description),
            weekly_availability=student_data.get("weekly_availability", existing_student.weekly_availability),
            preferred_modality=student_data.get("preferred_modality", existing_student.preferred_modality),
            experience_id=student_data.get("experience_id", existing_student.experience_id),
            date_of_birth=student_data.get("date_of_birth", existing_student.date_of_birth),
            embedding=student_data.get("embedding", existing_student.embedding)
        )

        return await self.student_repo.update(updated_student)

    async def delete_student(self, student_id: int) -> bool:
        return await self.student_repo.delete(student_id)

    async def validate_student_data(self, student_data: Dict[str, Any]) -> bool:
        logger.info(f"Validando datos del estudiante: {student_data}")

        # Validaciones básicas
        required_fields = ['name', 'email', 'date_of_birth', 'location', 'experience_id',
                         'weekly_availability', 'preferred_modality', 'career', 'academic_cycle', 
                         'main_motivation', 'description']

        for field in required_fields:
            if field not in student_data or not student_data[field]:
                logger.error(f"Campo faltante o vacío: {field}")
                return False

        # Validaciones específicas
        if student_data['weekly_availability'] <= 0 or student_data['weekly_availability'] > 40:
            logger.error(f"weekly_availability inválido: {student_data['weekly_availability']}")
            return False

        if student_data['academic_cycle'] <= 0 or student_data['academic_cycle'] > 12:
            logger.error(f"academic_cycle inválido: {student_data['academic_cycle']}")
            return False

        logger.info("Validación exitosa")
        return True

    async def check_email_exists(self, email: str) -> bool:
        student = await self.student_repo.find_by_email(email)
        return student is not None

    async def get_enriched_students(self) -> List[Student]:
        return await self.student_repo.get_enriched_students(self.session)
