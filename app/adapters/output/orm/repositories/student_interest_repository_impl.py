from typing import List
from sqlalchemy.future import select
from sqlalchemy import delete
from app.domain.entities.student_interest import StudentInterest
from app.domain.repositories.student_interest_repository import StudentInterestRepository
from app.adapters.output.orm.models.student_interest_model import StudentInterestModel

class StudentInterestRepositoryImpl(StudentInterestRepository):
    def __init__(self, session):
        self.session = session

    async def get_by_student_id(self, student_id: int) -> List[StudentInterest]:
        result = await self.session.execute(
            select(StudentInterestModel).where(StudentInterestModel.student_id == student_id)
        )
        models = result.scalars().all()
        interests = []
        for model in models:
            interests.append(
                StudentInterest(
                    student_id=model.student_id, 
                    interest_id=model.interest_id
                )
            )
        return interests

    async def exists(self, student_id: int, interest_id: int) -> bool:
        result = await self.session.execute(
            select(StudentInterestModel).where(
                StudentInterestModel.student_id == student_id,
                StudentInterestModel.interest_id == interest_id
            )
        )
        return result.scalar_one_or_none() is not None

    async def save(self, student_interest: StudentInterest) -> StudentInterest:
        exists = await self.exists(student_interest.student_id, student_interest.interest_id)
        if exists:
            return student_interest
        
        model = StudentInterestModel(
            student_id=student_interest.student_id,
            interest_id=student_interest.interest_id
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return StudentInterest(student_id=model.student_id, interest_id=model.interest_id)

    async def delete(self, student_id: int, interest_id: int) -> bool:
        result = await self.session.execute(
            select(StudentInterestModel).where(
                StudentInterestModel.student_id == student_id,
                StudentInterestModel.interest_id == interest_id
            )
        )
        model = result.scalar_one_or_none()
        if not model:
            return False

        await self.session.execute(
            delete(StudentInterestModel).where(
                StudentInterestModel.student_id == student_id,
                StudentInterestModel.interest_id == interest_id
            )
        )
        await self.session.commit()
        return True