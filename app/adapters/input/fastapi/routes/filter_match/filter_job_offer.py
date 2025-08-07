from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.future import select
from app.adapters.output.orm.models.job_offer_model import JobOfferModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session
from app.domain.services.job_offer_service import JobOfferService
from app.adapters.output.orm.repositories.job_offer_repository_impl import JobOfferRepositoryImpl
from app.domain.services.filter_match_service import FilterMatchService
from app.adapters.output.orm.repositories.filter_match_repository_impl import FilterMatchRepositoryImpl
from app.domain.entities.job_offer import JobOffer

from app.adapters.input.fastapi.schemas.filter_match_schema import FilterMatchResponse
from typing import List

router = APIRouter()


from app.application.factories.filter_match_factory import FilterMatchUseCaseFactory

@router.post("/filter/job_offer/preprocess_all_job_offer", response_model=List[FilterMatchResponse], tags=["AI Model"])
async def preprocess_all_job_offer(session: AsyncSession = Depends(get_session)):
    use_case = FilterMatchUseCaseFactory.create(session)
    service = FilterMatchService(FilterMatchRepositoryImpl(session), session)
    job_offer_repo = JobOfferRepositoryImpl(session)
    job_offers: List[JobOffer] = await job_offer_repo.get_all()
    job_offer_ids = [jo.id for jo in job_offers]
    try:
        processed = await service.preprocess_all_job_offers(job_offer_ids)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error en la API de IA: {str(e)}")
    return [FilterMatchResponse(**item) for item in processed]

@router.post("/filter/job_offer/preprocess_job_offer", response_model=FilterMatchResponse, tags=["AI Model"])
async def preprocess_job_offer(job_offer_id: int = Body(..., embed=True), session: AsyncSession = Depends(get_session)):
    use_case = FilterMatchUseCaseFactory.create(session)
    service = FilterMatchService(FilterMatchRepositoryImpl(session), session)
    job_offer_repo = JobOfferRepositoryImpl(session)
    job_offer = await job_offer_repo.find_by_id(job_offer_id)
    if not job_offer:
        raise HTTPException(status_code=404, detail="Job offer not found")
    try:
        processed = await service.preprocess_job_offer(job_offer_id)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error en la API de IA: {str(e)}")
    if not processed:
        raise HTTPException(status_code=500, detail="No se pudo obtener el embedding")
    return FilterMatchResponse(**processed)