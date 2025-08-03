from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from app.adapters.output.orm.models.job_offer_model import JobOfferModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session
from app.adapters.output.orm.repositories.job_offer_repository_impl import JobOfferRepositoryImpl
from app.domain.entities.job_offer import JobOffer
from app.domain.services.filter_match_service import FilterMatchService
from fastapi import Body
from typing import List

router = APIRouter()

@router.post("/filter/job_offer/preprocess_all_job_offer", response_model=dict, tags=["AI Model"])
async def preprocess_all_job_offer(session: AsyncSession = Depends(get_session)):
    repo = JobOfferRepositoryImpl(session)
    job_offers: List[JobOffer] = await repo.get_all()
    service = FilterMatchService(None)
    try:
        processed = await service.preprocess_all_job_offers(job_offers, session)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error en la API de IA: {str(e)}")

    id_to_embedding = {item["job_offer_id"]: item["embedding"] for item in processed}

    for job_offer in job_offers:
        embedding = id_to_embedding.get(job_offer.id)
        if embedding is not None:
            result = await session.execute(
                select(JobOfferModel).where(JobOfferModel.id == job_offer.id)
            )
            model = result.scalar_one_or_none()
            if model:
                model.embedding = embedding
    await session.commit()
    return {"message": "Embeddings generados y guardados correctamente", "total": len(job_offers)}

@router.post("/filter/job_offer/preprocess_job_offer", response_model=dict, tags=["AI Model"])
async def preprocess_job_offer(job_offer_id: int = Body(..., embed=True), session: AsyncSession = Depends(get_session)):
    repo = JobOfferRepositoryImpl(session)
    job_offer = await repo.find_by_id(job_offer_id)
    if not job_offer:
        raise HTTPException(status_code=404, detail="Job offer not found")

    service = FilterMatchService(None)
    try:
        processed = await service.preprocess_job_offer(job_offer, session)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error en la API de IA: {str(e)}")

    embedding = None
    if processed and isinstance(processed, list) and len(processed) > 0:
        embedding = processed[0].get("embedding")
    elif processed and isinstance(processed, dict):
        embedding = processed.get("embedding")
    if embedding is None:
        raise HTTPException(status_code=500, detail="No se pudo obtener el embedding")

    result = await session.execute(
        select(JobOfferModel).where(JobOfferModel.id == job_offer.id)
    )
    model = result.scalar_one_or_none()
    if model:
        model.embedding = embedding
    await session.commit()
    return {"message": "Embedding generado y guardado correctamente", "job_offer_id": job_offer.id}
