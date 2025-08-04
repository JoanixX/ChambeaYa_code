from fastapi import APIRouter, Body
from app.infraestructure.database.connection import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.adapters.output.orm.repositories.job_offer_repository_impl import JobOfferRepositoryImpl
from app.adapters.output.orm.repositories.student_repository_impl import StudentRepositoryImpl
from app.domain.services.match_job_student_service import MatchJobStudentService
from fastapi import HTTPException, Depends

router = APIRouter()

@router.post("/aimodel/job_offer/best_students/{job_offer_id}", response_model=dict, tags=["AI Model"])
async def best_students(job_offer_id: int, session: AsyncSession = Depends(get_session)):
    job_offer_repo = JobOfferRepositoryImpl(session)
    job_offer = await job_offer_repo.find_by_id(job_offer_id)
    if not job_offer:
        raise HTTPException(status_code=404, detail="Job offer not found")

    student_repo = StudentRepositoryImpl(session)
    students = await student_repo.get_all()
    service = MatchJobStudentService()
    try:
        response = await service.match_best_from_offer(job_offer, students)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

    return response