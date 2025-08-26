from typing import List, Dict
import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session

from app.adapters.input.fastapi.schemas.job_offer_schema import (JobOfferCreate, JobOfferResponse)
from app.application.factories.job_offer_factory import JobOfferUseCaseFactory

router = APIRouter()
# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/register/job_offer", response_model=dict, tags=["Job Offer"])
async def register_job_offer(request: Request, job_offer: JobOfferCreate, session: AsyncSession = Depends(get_session)):
    try:
        body = await request.body()
        logger.info(f"Body recibido: {body.decode()}")
        logger.info(f"Iniciando registro de oferta de trabajo: {job_offer.title}")

        job_offer_use_case = JobOfferUseCaseFactory(session).build()

        logger.info("Ejecutando caso de uso...")
        result = await job_offer_use_case.register_job_offer(job_offer.dict())
        logger.info(f"Oferta de trabajo registrada con éxito: {result}")
        return JSONResponse(content=result)
    
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error al registrar oferta de trabajo: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/job_offer/all", response_model=List[dict], tags=["Job Offer"])
async def get_all_job_offers(session: AsyncSession = Depends(get_session)):
    try:
        job_offer_use_case = JobOfferUseCaseFactory(session).build()
        job_offers = await job_offer_use_case.get_all_job_offers()
        return [JobOfferResponse(**j.__dict__).model_dump() for j in job_offers]
    
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/job_offer/{job_offer_id}", response_model=dict, tags=["Job Offer"])
async def get_job_offer(job_offer_id: int, session: AsyncSession = Depends(get_session)):
    try:
        job_offer_use_case = JobOfferUseCaseFactory(session).build()
        job_offer = await job_offer_use_case.get_job_offer(job_offer_id)
        return JobOfferResponse(**job_offer.__dict__).model_dump()
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/company/{company_id}/job_offers", response_model=List[Dict], tags=["Job Offer", "Company"])
async def get_company_job_offers(company_id: int, session: AsyncSession = Depends(get_session)):
    try:
        job_offer_use_case = JobOfferUseCaseFactory(session).build()
        job_offers = await job_offer_use_case.get_company_job_offers(company_id)
        return [JobOfferResponse(**j.__dict__).model_dump() for j in job_offers]
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.put("/job_offer/{job_offer_id}", response_model=dict, tags=["Job Offer"])
async def update_job_offer_endpoint(job_offer_id: int, job_offer: JobOfferCreate, session: AsyncSession = Depends(get_session)):
    try:
        job_offer_use_case = JobOfferUseCaseFactory(session).build()
        updated = await job_offer_use_case.update_job_offer(job_offer_id, job_offer.dict())
        return JobOfferResponse(**updated.__dict__).model_dump()
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.delete("/job_offer/{job_offer_id}", response_model=dict, tags=["Job Offer"])
async def delete_job_offer_endpoint(job_offer_id: int, session: AsyncSession = Depends(get_session)):
    try:
        job_offer_use_case = JobOfferUseCaseFactory(session).build()
        deleted = await job_offer_use_case.delete_job_offer(job_offer_id)
        return deleted
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")