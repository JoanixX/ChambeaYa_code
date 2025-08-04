from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session
from app.adapters.output.orm.repositories.student_repository_impl import StudentRepositoryImpl
from app.adapters.output.orm.repositories.job_offer_repository_impl import JobOfferRepositoryImpl
from app.domain.services.match_job_student_service import MatchJobStudentService

router = APIRouter()

@router.post("/aimodel/student/best_job_offers/{student_id}", response_model=dict, tags=["AI Model"])
async def best_job_offers(student_id: int, session: AsyncSession = Depends(get_session)):
    student_repo = StudentRepositoryImpl(session)
    student = await student_repo.find_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    job_offer_repo = JobOfferRepositoryImpl(session)
    job_offers = await job_offer_repo.get_all()

    service = MatchJobStudentService()
    try:
        response = await service.match_best_from_student(student, job_offers)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

    return response
