from typing import List
import logging
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session

from app.adapters.input.fastapi.schemas.filter_match_schema import (FilterMatchCreate, FilterMatchResponse)
from app.application.factories.filter_match_factory import FilterMatchUseCaseFactory
from app.domain.entities.job_offer import JobOffer
from app.adapters.output.orm.repositories.job_offer_repository_impl import JobOfferRepositoryImpl

router = APIRouter()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/filter/job_offer/preprocess_all_job_offer", response_model=List[FilterMatchResponse], tags=["AI Model"])
async def preprocess_all_job_offer(session: AsyncSession = Depends(get_session)):
    use_case = FilterMatchUseCaseFactory(session).build()
    job_offer_repo = JobOfferRepositoryImpl(session)
    job_offers: List[JobOffer] = await job_offer_repo.get_all()
    job_offer_ids = [jo.id for jo in job_offers]
    try:
        processed = await use_case.preprocess_all_job_offers(job_offer_ids)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error en la API de IA: {str(e)}")
    # Filtrar duplicados por job_offer_id y asegurar campos opcionales
    seen_ids = set()
    response_list = []
    for item in processed:
        item_id = item.get("job_offer_id") or item.get("id")
        if item_id is not None and item_id in seen_ids:
            continue
        seen_ids.add(item_id)
        response_list.append(FilterMatchResponse(**item))
    return response_list

@router.post("/filter/job_offer/preprocess_job_offer", response_model=FilterMatchResponse, tags=["AI Model"])
async def preprocess_job_offer(job_offer_id: int = Body(..., embed=True), session: AsyncSession = Depends(get_session)):
    use_case = FilterMatchUseCaseFactory(session).build()
    job_offer_repo = JobOfferRepositoryImpl(session)
    job_offer = await job_offer_repo.find_by_id(job_offer_id)
    if not job_offer:
        raise HTTPException(status_code=404, detail="Job offer not found")
    try:
        processed = await use_case.preprocess_job_offer(job_offer_id)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error en la API de IA: {str(e)}")
    if not processed:
        raise HTTPException(status_code=500, detail="No se pudo obtener el embedding")
    return FilterMatchResponse(**processed)
