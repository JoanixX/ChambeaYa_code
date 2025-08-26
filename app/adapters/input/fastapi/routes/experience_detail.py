from typing import List, Dict
import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session

from app.adapters.input.fastapi.schemas.experience_detail_schema import (ExperienceDetailCreate, ExperienceDetailResponse)
from app.application.factories.experience_detail_factory import ExperienceDetailUseCaseFactory

router = APIRouter()
# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/register/experience_detail", response_model=dict, tags=["Experience Detail"])
async def register_experience_detail(request: Request, experience_detail: ExperienceDetailCreate , session: AsyncSession = Depends(get_session)):
    try:
        body = await request.body()
        logger.info(f"Body recibido: {body.decode()}")
        logger.info(f"Iniciando registro de experiencia: {experience_detail.name}")

        experience_detail_use_case = ExperienceDetailUseCaseFactory(session).build()

        logger.info("Ejecutando caso de uso...")
        result = await experience_detail_use_case.register_experience_detail(experience_detail.dict())
        logger.info(f"Experiencia registrada con éxito: {result}")
        return JSONResponse(content=result)
    
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error al registrar experiencia: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.post("/experience_detail/all", response_model=List[dict], tags=["Experience Detail"])
async def get_all_experience_details(session: AsyncSession = Depends(get_session)):
    try:
        experience_detail_use_case = ExperienceDetailUseCaseFactory(session).build()
        experience_details = await experience_detail_use_case.get_all_experience_details()
        return [ExperienceDetailResponse(**ed.__dict__).model_dump() for ed in experience_details]
    
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/experience_detail/{experience_detail_id}", response_model=dict, tags=["Experience Detail"])
async def get_experience_detail(experience_detail_id: int, session: AsyncSession = Depends(get_session)):
    try:
        experience_detail_use_case = ExperienceDetailUseCaseFactory(session).build()
        experience_detail = await experience_detail_use_case.get_experience_detail(experience_detail_id)
        return ExperienceDetailResponse(**experience_detail.__dict__).model_dump()
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/student/{student_id}/experience_details", response_model=List[Dict], tags=["Experience Detail", "Student"])
async def get_student_experience_details(student_id: int, session: AsyncSession = Depends(get_session)):
    try:
        experience_detail_use_case = ExperienceDetailUseCaseFactory(session).build()
        experience_details = await experience_detail_use_case.get_student_experience_details(student_id)
        return [ExperienceDetailResponse(**ed.__dict__).model_dump() for ed in experience_details]
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/job_offer/{job_offer_id}/experience_details", response_model=List[Dict], tags=["Experience Detail", "Job Offer"])
async def get_job_offer_experience_details(job_offer_id: int, session: AsyncSession = Depends(get_session)):
    try:
        experience_detail_use_case = ExperienceDetailUseCaseFactory(session).build()
        experience_details = await experience_detail_use_case.get_job_offer_experience_details(job_offer_id)
        return [ExperienceDetailResponse(**ed.__dict__).model_dump() for ed in experience_details]
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
@router.put("/experience_detail/{experience_detail_id}", response_model=dict, tags=["Experience Detail"])
async def update_experience_detail(experience_detail_id: int, experience_detail: ExperienceDetailCreate, session: AsyncSession = Depends(get_session)):
    try:
        experience_detail_use_case = ExperienceDetailUseCaseFactory(session).build()
        updated = await experience_detail_use_case.update_experience_detail(experience_detail_id, experience_detail.dict())
        return ExperienceDetailResponse(**updated.__dict__).model_dump()
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
@router.delete("/experience_detail/{experience_detail_id}", response_model=dict, tags=["Experience Detail"])
async def delete_experience_detail(experience_detail_id: int, session: AsyncSession = Depends(get_session)):
    try:
        experience_detail_use_case = ExperienceDetailUseCaseFactory(session).build()
        deleted = await experience_detail_use_case.delete_experience_detail(experience_detail_id)
        return deleted
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")