from app.application.ports.student_interest_port import StudentInterestPort
from app.domain.entities.student_interest import StudentInterest
from app.domain.services.student_interest_service import StudentInterestService
from typing import Dict, Any, List

class StudentInterestUseCase:
    def __init__(self, student_interest_port: StudentInterestPort, student_interest_service: StudentInterestService):
        self.student_interest_port = student_interest_port
        self.student_interest_service = student_interest_service

    async def get_student_interests(self, student_id: int) -> List[StudentInterest]:
        return await self.student_interest_port.get_student_interests(student_id)

    async def add_student_interest(self, student_interest: StudentInterest) -> StudentInterest:
        interest_id = await self.student_interest_port.add_student_interest(student_interest) 

        if not interest_id:
            raise ValueError("Error al agregar el interés al estudiante")

        return interest_id
    
    async def delete_student_interest(self, student_id: int, interest_id: int) -> Dict[str, Any]:
        success = await self.student_interest_port.delete_student_interest(student_id, interest_id)

        if not success:
            raise ValueError(f"Error al eliminar el interés con ID {interest_id} del estudiante con ID {student_id}")

        return {
            "message": "Interés eliminado exitosamente del estudiante"
        }