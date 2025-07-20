from app.application.ports.register_student_port import RegisterStudentPort
from app.domain.entities.student import Student
from app.domain.services.student_profile_evaluator import StudentProfileEvaluator

class RegisterStudentUseCase:
    def __init__(self, register_student_port: RegisterStudentPort, student_evaluator: StudentProfileEvaluator):
        self.register_student_port = register_student_port
        self.student_evaluator = student_evaluator

    async def execute(self, student_data: dict) -> dict:
        # Validar datos
        if not await self.register_student_port.validate_student_data(student_data):
            raise ValueError("Datos de estudiante inválidos")
        
        # Verificar email único
        if await self.register_student_port.check_email_exists(student_data["email"]):
            raise ValueError("El email ya está registrado")
        
        # Crear entidad de dominio
        student = Student(
            name=student_data["name"],
            email=student_data["email"],
            date_of_birth=student_data["date_of_birth"],
            experience_id=student_data["experience_id"],
            location=student_data["location"],
            weekly_availability=student_data["weekly_availability"],
            preferred_modality=student_data["preferred_modality"],
            career=student_data["career"],
            academic_cycle=student_data["academic_cycle"],
            main_motivation=student_data["main_motivation"],
            description=student_data["description"]
        )
        
        # Registrar estudiante
        saved_student = await self.register_student_port.register_student(student)
        
        # Evaluar perfil
        evaluation = await self.student_evaluator.evaluate_student_profile(saved_student.id)
        
        return {
            "student_id": saved_student.id,
            "registration_success": True,
            "profile_evaluation": evaluation
        }
