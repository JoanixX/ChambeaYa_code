from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session
from app.domain.repositories.job_offer_repository import get_all_job_offers
from app.domain.entities.job_offer import JobOffer
from typing import List

router = APIRouter()

@router.get("/job_offer/all", response_model=List[dict])
async def get_all_job_offers_endpoint(session: AsyncSession = Depends(get_session)):
    job_offers: List[JobOffer] = await get_all_job_offers(session)
    result = []
    for j in job_offers:
        result.append({
            "id": j.id,
            "company_id": j.company_id,
            "title": j.title,
            "description": j.description,
            "required_hours": j.required_hours,
            "approximated_salary": j.approximated_salary,
            "duration": j.duration,
            "start_date": j.start_date.isoformat() if j.start_date else None,
            "area_id": j.area_id,
            "experience_id": j.experience_id,
            "modality": j.modality,
            "requirements": j.requirements,
            "embedding": j.embedding
        })
    return result
