from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session
from app.domain.repositories.job_offer_repository import get_all_job_offers
from app.domain.entities.job_offer import JobOffer
from app.infraestructure.ai_client.ai_connection import preprocess_all_job_offers
from typing import List

router = APIRouter()

@router.post("/filter/job_offer/preprocess_all_job_offer")
async def preprocess_all_job_offer(session: AsyncSession = Depends(get_session)):
    job_offers: List[JobOffer] = await get_all_job_offers(session)

    job_offers_data = []
    for j in job_offers:
        job_offers_data.append({
            "id": j.id,
            "title": j.title,
            "description": j.description,
            "required_hours": j.required_hours,
            "approximated_salary": j.approximated_salary,
            "duration": j.duration,
            "start_date": j.start_date.isoformat() if j.start_date else None,
            "area_id": j.area_id,
            "experience_id": j.experience_id,
            "modality": j.modality,
            "required_skills": [],
            "embedding": None
        })

    try:
        processed = await preprocess_all_job_offers(job_offers_data)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error en la API de IA: {str(e)}")

    id_to_embedding = {item["job_offer_id"]: item["embedding"] for item in processed}

    for job_offer in job_offers:
        embedding = id_to_embedding.get(job_offer.id)
        if embedding:
            job_offer.embedding = embedding

    await session.commit()

    return {"message": "Embeddings generados y guardados correctamente", "total": len(job_offers)}
