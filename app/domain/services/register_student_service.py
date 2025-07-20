from app.domain.entities.student import Student
from app.domain.repositories.student_repository import StudentRepository
from app.application.ports.register_student_port import RegisterStudentPort

class RegisterStudentService:
    def __init__(self, student_repo: StudentRepository, register_student_port: RegisterStudentPort):
        self.student_repo = student_repo
        self.register_student_port = register_student_port

    async def register_student(self, student_data: dict):
        # Validaciones de negocio básicas
        if await self.student_repo.find_by_email(student_data["email"]):
            raise ValueError("El email ya está registrado")
        
        # Crear entidad de dominio con constructor correcto
        student = Student(
            id=0,  # Se asignará automáticamente por la base de datos
            name=student_data["name"],
            email=student_data["email"],
            career=student_data["career"],
            academic_cycle=student_data["academic_cycle"],
            location=student_data["location"],
            main_motivation=student_data["main_motivation"],
            description=student_data["description"],
            weekly_availability=student_data["weekly_availability"],
            preferred_modality=student_data["preferred_modality"],
            experience_id=student_data.get("experience_id", None),  # Opcional
            date_of_birth=student_data["date_of_birth"],
            embedding={}  # Embedding vacío por defecto
        )
        
        # Guardar estudiante usando el repositorio directamente
        saved_model = await self.student_repo.save(student)
        if saved_model:
            return saved_model.id  # Retornar solo el ID
        else:
            raise ValueError("Error al guardar el estudiante")