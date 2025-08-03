from app.application.ports.student_skill_port import StudentSkillPort
from app.domain.entities.student_skill import StudentSkill
from app.domain.services.student_skill_service import StudentSkillService
from typing import Dict, Any, List

class StudentSkillUseCase:
    def __init__(self, student_skill_port: StudentSkillPort, student_skill_service: StudentSkillService):
        self.student_skill_port = student_skill_port
        self.student_skill_service = student_skill_service

    async def get_student_skills(self, student_id: int) -> List[StudentSkill]:
        return await self.student_skill_port.get_student_skills(student_id)

    async def add_student_skill(self, student_skill: StudentSkill) -> StudentSkill:
        student_skill_id = await self.student_skill_port.add_student_skill(student_skill) 

        if not student_skill_id:
            raise ValueError("Error al agregar la habilidad al estudiante")

        return student_skill_id
    
    async def delete_student_skill(self, student_id: int, skill_id: int) -> Dict[str, Any]:
        success = await self.student_skill_port.delete_student_skill(student_id, skill_id)

        if not success:
            raise ValueError(f"Error al eliminar la habilidad con ID {skill_id} del estudiante con ID {student_id}")

        return {
            "message": "Habilidad eliminada exitosamente del estudiante"
        }