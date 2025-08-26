from app.application.ports.student_port import StudentPort
from app.domain.entities.student import Student
from app.domain.services.student_service import StudentService
from typing import Dict, Any, List

class StudentUseCase:
    def __init__(self, student_port: StudentPort, student_service: StudentService):
        self.student_port = student_port
        self.student_service = student_service

    async def get_enriched_students(self) -> List[Student]:
        return await self.student_port.get_enriched_students()

    async def register_student(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        if not await self.student_port.validate_student_data(student_data):
            raise ValueError("Datos de estudiante inválidos")

        student_id = await self.student_service.register_student(student_data)

        if not student_id:
            raise ValueError("Error al guardar el estudiante")

        return {
            "student_id": student_id,
            "registration_success": True,
            "message": "Estudiante registrado exitosamente"
        }

    async def get_student(self, student_id: int) -> Student:
        student = await self.student_port.get_student(student_id)
        if not student:
            raise ValueError(f"Estudiante con ID {student_id} no encontrado")
        return student

    async def get_all_students(self) -> List[Student]:
        return await self.student_port.get_all_students()

    async def update_student(self, student_id: int, student_data: Dict[str, Any]) -> Student:
        if not await self.student_port.validate_student_data(student_data):
            raise ValueError("Datos de estudiante inválidos")

        student = await self.student_port.get_student(student_id)
        if not student:
            raise ValueError(f"Estudiante con ID {student_id} no encontrado")

        updated_student = await self.student_port.update_student(student_id, student_data)
        if not updated_student:
            raise ValueError(f"Error al actualizar estudiante con ID {student_id}")

        return updated_student

    async def delete_student(self, student_id: int) -> Dict[str, Any]:
        student = await self.student_port.get_student(student_id)
        if not student:
            raise ValueError(f"Estudiante con ID {student_id} no encontrado")

        success = await self.student_port.delete_student(student_id)
        if not success:
            raise ValueError(f"Error al eliminar estudiante con ID {student_id}")

        return {
            "message": "Estudiante eliminado exitosamente"
        }