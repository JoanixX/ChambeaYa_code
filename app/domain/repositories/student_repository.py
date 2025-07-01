from app.domain.entities.student import Student
from sqlalchemy.future import select

async def get_all_students(session):
    result = await session.execute(select(Student))
    return result.scalars().all()
