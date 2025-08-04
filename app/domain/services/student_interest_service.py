from app.domain.entities.student_interest import StudentInterest
from app.domain.repositories.student_interest_repository import StudentInterestRepository
from typing import List

class StudentInterestService:
    def __init__(self, student_interest_repo: StudentInterestRepository):
        self.student_interest_repo = student_interest_repo

    async def add_student_interest(self, student_interest: StudentInterest) -> StudentInterest:
        exists = await self.student_interest_repo.exists(student_interest.student_id, student_interest.interest_id)

        if exists:
            raise ValueError("El estudiante ya tiene este interes asignado")

        saved_model = await self.student_interest_repo.save(student_interest)

        if saved_model:
            return saved_model
        else:
            raise ValueError("Error al guardar el interes del estudiante")

    async def get_student_interests(self, student_id: int) -> List[StudentInterest]:
        return await self.student_interest_repo.get_by_student_id(student_id)

    async def delete_student_interest(self, student_id: int, interest_id: int) -> bool:
        return await self.student_interest_repo.delete(student_id, interest_id)