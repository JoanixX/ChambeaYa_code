from app.domain.entities.student import Student
from app.domain.repositories.student_repository import StudentRepository
from typing import Dict, Any, Optional

class StudentService:
    def __init__(self, student_repo: StudentRepository):
        self.student_repo = student_repo

    async def get_enriched_students(self) -> list:
        return await self.student_repo.get_enriched_students(self.student_repo.session)

    async def register_student(self, student_data: Dict[str, Any]) -> int:
        student = self.student_entity(student_data)

        saved_model = await self.student_repo.save(student)
        if saved_model:
            return saved_model.id
        else:
            raise ValueError("Error al guardar el estudiante")

    async def get_student(self, student_id: int) -> Optional[Student]:
        return await self.student_repo.find_by_id(student_id)

    async def get_all_students(self) -> list[Student]:
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

        await self.student_repo.update(updated_student)
        return updated_student

    async def delete_student(self, student_id: int) -> bool:
        return await self.student_repo.delete(student_id)

    def student_entity(self, student_data: Dict[str, Any]) -> Student:
        return Student(
            id=0,  # Se asignará automáticamente por la base de datos
            name=student_data.get("name", None),
            email=student_data.get("email", None),
            career=student_data.get("career", None),
            academic_cycle=student_data.get("academic_cycle", None),
            location=student_data.get("location", None),
            main_motivation=student_data.get("main_motivation", None),
            description=student_data.get("description", None),
            weekly_availability=student_data.get("weekly_availability", None),
            preferred_modality=student_data.get("preferred_modality", None),
            experience_id=student_data.get("experience_id", None),
            date_of_birth=student_data.get("date_of_birth", None),
            embedding=student_data.get("embedding", {})
        )