from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.infraestructure.database.connection import get_session
from app.domain.entities.student import Student
from app.domain.entities.job_offer import JobOffer
from app.domain.services.match_job_student_service import MatchJobStudentService

router = APIRouter()

@router.post("/aimodel/student/best_job_offers/{student_id}", response_model=dict, tags=["AI Model"])
async def best_job_offers(student_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    result = await session.execute(select(JobOffer).where(JobOffer.embedding.is_not(None)))
    job_offers = result.scalars().all()

    service = MatchJobStudentService()
    try:
        response = await service.match_best(student, job_offers)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error en la API de IA: {str(e)}")

    return response
