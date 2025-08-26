from typing import Dict, Any, Optional
from datetime import datetime

from app.domain.entities.student import Student
from app.domain.repositories.student_repository import StudentRepository

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
            career=student_data.get("career", existing_student.career),
            academic_cycle=student_data.get("academic_cycle", existing_student.academic_cycle),
            weekly_availability=student_data.get("weekly_availability", existing_student.weekly_availability),
            preferred_modality=student_data.get("preferred_modality", existing_student.preferred_modality),
            embedding=student_data.get("embedding", existing_student.embedding)
        )

        await self.student_repo.update(updated_student)
        return updated_student

    async def delete_student(self, student_id: int) -> bool:
        return await self.student_repo.delete(student_id)

    def student_entity(self, student_data: Dict[str, Any]) -> Student:
        if 'created_at' not in student_data:
            student_data['created_at'] = datetime.now()
        if 'updated_at' not in student_data:
            student_data['updated_at'] = datetime.now()
        return Student(
            id=0,  # Se asignará automáticamente por la base de datos
            career=student_data.get("career", None),
            academic_cycle=student_data.get("academic_cycle", None),
            weekly_availability=student_data.get("weekly_availability", None),
            preferred_modality=student_data.get("preferred_modality", None),
            embedding=student_data.get("embedding", {}),
            created_at=student_data['created_at'],
            updated_at=student_data['updated_at']
         )