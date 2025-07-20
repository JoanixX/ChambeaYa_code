from app.domain.entities.student import Student
from app.domain.repositories.student_repository import StudentRepository
from app.application.ports.register_student_port import RegisterStudentPort

class StudentProfileEvaluator:
    def __init__(self, student_repo: StudentRepository, register_student_port: RegisterStudentPort):
        self.student_repo = student_repo
        self.register_student_port = register_student_port

    async def register_student(self, student_data: dict):
        # Validaciones de negocio
        if await self.student_repo.find_by_email(student_data["email"]):
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
        
        # Guardar estudiante
        saved_student = await self.student_repo.save(student)
        return saved_student

    async def evaluate_student_profile(self, student_id: int):
        student = await self.student_repo.find_by_id(student_id)
        if not student:
            raise ValueError("Estudiante no encontrado")
        
        # Lógica de evaluación del perfil
        evaluation = {
            "student_id": student.id,
            "completeness_score": self._calculate_completeness(student),
            "match_potential": self._calculate_match_potential(student),
            "recommendations": self._generate_recommendations(student)
        }
        
        return evaluation

    def _calculate_completeness(self, student: Student) -> float:
        # Lógica para calcular qué tan completo está el perfil
        required_fields = [
            student.name, student.email, student.career, 
            student.location, student.description, student.main_motivation
        ]
        filled_fields = sum(1 for field in required_fields if field and str(field).strip())
        return (filled_fields / len(required_fields)) * 100

    def _calculate_match_potential(self, student: Student) -> float:
        # Lógica para calcular el potencial de matching
        score = 0.0
        
        # Evaluar disponibilidad semanal
        if student.weekly_availability >= 20:
            score += 30
        elif student.weekly_availability >= 15:
            score += 20
        elif student.weekly_availability >= 10:
            score += 10
        
        # Evaluar experiencia
        if student.experience_id <= 2:  # Asumiendo que IDs menores son más experiencia
            score += 40
        elif student.experience_id <= 4:
            score += 25
        else:
            score += 10
        
        # Evaluar ciclo académico
        if 6 <= student.academic_cycle <= 10:  # Ciclos intermedios
            score += 30
        else:
            score += 15
        
        return min(score, 100.0)

    def _generate_recommendations(self, student: Student) -> list[str]:
        recommendations = []
        
        if student.weekly_availability < 15:
            recommendations.append("Considera aumentar tu disponibilidad semanal para más oportunidades")
        
        if student.academic_cycle < 6:
            recommendations.append("Es recomendable tener al menos 6 ciclos para mejores oportunidades")
        
        if not student.description or len(student.description) < 50:
            recommendations.append("Completa mejor tu descripción para destacar tus habilidades")
        
        return recommendations