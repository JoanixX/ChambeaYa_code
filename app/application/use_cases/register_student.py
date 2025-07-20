from app.application.ports.register_student_port import RegisterStudentPort
from app.domain.entities.student import Student
from app.domain.services.register_student_service import RegisterStudentService

class RegisterStudentUseCase:
    def __init__(self, register_student_port: RegisterStudentPort, register_student_service: RegisterStudentService):
        self.register_student_port = register_student_port
        self.register_student_service = register_student_service

    async def execute(self, student_data: dict) -> dict:
        # Validar datos
        if not await self.register_student_port.validate_student_data(student_data):
            raise ValueError("Datos de estudiante inválidos")
        
        # Verificar email único
        if await self.register_student_port.check_email_exists(student_data["email"]):
            raise ValueError("El email ya está registrado")
        
        # Registrar estudiante usando el servicio de dominio
        student_id = await self.register_student_service.register_student(student_data)
        
        # Verificar que el estudiante se guardó correctamente
        if not student_id:
            raise ValueError("Error al guardar el estudiante")
        
        return {
            "student_id": student_id,
            "registration_success": True,
            "message": "Estudiante registrado exitosamente"
        }