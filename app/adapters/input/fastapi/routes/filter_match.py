from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.infraestructure.database.connection import get_session
from app.domain.entities.filter_match import FilterMatch
from app.domain.entities.student import Student
from app.domain.entities.job_offer import JobOffer
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()

class FilterMatchInput(BaseModel):
    student_id: int = Field(..., description="ID del estudiante")
    job_offer_id: int = Field(..., description="ID de la oferta de trabajo")
    model_score: float = Field(..., description="Score del modelo")
    status: str = Field(..., description="Estado del filtro")
    stage: int = Field(..., description="Fase de filtrado (1 o 2)")

@router.post("/filter_match")
async def create_filter_match(payload: FilterMatchInput, session: AsyncSession = Depends(get_session)):
    # Verificar existencia de estudiante y oferta
    student = await session.get(Student, payload.student_id)
    job_offer = await session.get(JobOffer, payload.job_offer_id)
    if not student or not job_offer:
        raise HTTPException(status_code=404, detail="Estudiante u oferta no encontrada")
    filter_match = FilterMatch(
        student_id=payload.student_id,
        job_offer_id=payload.job_offer_id,
        model_score=payload.model_score,
        status=payload.status,
        filtered_at=datetime.utcnow(),
        stage=payload.stage
    )
    session.add(filter_match)
    await session.commit()
    return {"message": "FilterMatch creado correctamente"}

@router.get("/filter_match/student/{student_id}")
async def get_filter_matches_by_student(student_id: int, stage: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(FilterMatch).where(FilterMatch.student_id == student_id, FilterMatch.stage == stage))
    matches = result.scalars().all()
    return matches

@router.get("/filter_match/job_offer/{job_offer_id}")
async def get_filter_matches_by_job_offer(job_offer_id: int, stage: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(FilterMatch).where(FilterMatch.job_offer_id == job_offer_id, FilterMatch.stage == stage))
    matches = result.scalars().all()
    return matches

