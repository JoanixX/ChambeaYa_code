from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.student_interest import StudentInterest
from app.adapters.output.orm.repositories.student_interest_repository_impl import StudentInterestRepositoryImpl
from app.application.ports.student_interest_port import StudentInterestPort

class StudentInterestPortImpl(StudentInterestPort):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.student_interest_repo = StudentInterestRepositoryImpl(session)

    async def add_student_interest(self, student_interest: StudentInterest) -> StudentInterest:
        return await self.student_interest_repo.save(student_interest)

    async def get_student_interests(self, student_id: int) -> List[StudentInterest]:
        return await self.student_interest_repo.get_by_student_id(student_id)
    
    async def delete_student_interest(self, student_id: int, interest_id: int) -> bool:
        return await self.student_interest_repo.delete(student_id, interest_id)
    
    async def student_interest_exists(self, student_id: int, interest_id: int) -> bool:
        return await self.student_interest_repo.exists(student_id, interest_id)