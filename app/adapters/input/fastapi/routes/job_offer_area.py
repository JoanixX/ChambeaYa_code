from typing import List
import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session

from app.domain.entities.job_offer_area import JobOfferArea
from app.adapters.input.fastapi.schemas.job_offer_area_schema import (JobOfferAreaResponse, JobOfferAreaCreate)
from app.application.factories.job_offer_area_factory import JobOfferAreaUseCaseFactory

router = APIRouter()
# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
    
@router.post("/job_offer/job_offer_area", response_model=JobOfferAreaResponse, tags=["Job Offer", "Area"])
async def add_job_offer_area(request: Request, job_offer_area: JobOfferAreaCreate, session: AsyncSession = Depends(get_session)):
    try:
        job_offer_area_use_case = JobOfferAreaUseCaseFactory(session).build()

        job_offer_area  = JobOfferArea(
            job_offer_id=job_offer_area.job_offer_id,
            area_id=job_offer_area.area_id
        )

        result = await job_offer_area_use_case.add_job_offer_area(job_offer_area)
        return JobOfferAreaResponse(job_offer_id=result.job_offer_id, area_id=result.area_id)
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error al agregar area a la oferta de trabajo: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/job_offer/{job_offer_id}/areas", response_model=List[JobOfferAreaResponse], tags=["Job Offer", "Area"])
async def get_job_offer_areas(job_offer_id: int, session: AsyncSession = Depends(get_session)):
    try:
        job_offer_area_use_case = JobOfferAreaUseCaseFactory(session).build()

        areas = await job_offer_area_use_case.get_job_offer_areas(job_offer_id)
        return [area.__dict__ for area in areas]
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
@router.delete("/job_offer/{job_offer_id}/area/{area_id}", response_model=dict, tags=["Job Offer", "Area"])
async def delete_job_offer_area(job_offer_id: int, area_id: int, session: AsyncSession = Depends(get_session)):
    try:
        job_offer_area_use_case = JobOfferAreaUseCaseFactory(session).build()
        deleted = await job_offer_area_use_case.delete_job_offer_area(job_offer_id, area_id)

        return deleted
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")