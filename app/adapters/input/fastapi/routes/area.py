from typing import List, Optional
import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session

from app.adapters.input.fastapi.schemas.area_schema import (AreaCreate, AreaResponse)
from app.application.factories.area_factory import AreaUseCaseFactory

router = APIRouter()
# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/register/area", response_model=AreaResponse, tags=["Area"])
async def register_area(request: Request, area: AreaCreate, session: AsyncSession = Depends(get_session)):
    try:
        body = await request.body()
        logger.info(f"Body recibido: {body.decode()}")
        logger.info(f"Iniciando registro de area: {area.name}")
        
        area_use_case = AreaUseCaseFactory(session).build()

        logger.info("Ejecutando caso de uso...")
        area_id = await area_use_case.register_area(area.dict())
        area_obj = await area_use_case.get_area(area_id)
        
        logger.info(f"Area registrada exitosamente: {area_obj}")
        return area_obj
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error interno del servidor: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/area/all", response_model=List[AreaResponse], tags=["Area"])
async def get_all_areas(session: AsyncSession = Depends(get_session)):
    try:
        area_use_case = AreaUseCaseFactory(session).build()
        areas = await area_use_case.get_all_areas()

        return areas
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/area/{area_id}", response_model=AreaResponse, tags=["Area"])
async def get_area_by_id(area_id: int, session: AsyncSession = Depends(get_session)):
    try:
        area_use_case = AreaUseCaseFactory(session).build()
        area = await area_use_case.get_area(area_id)

        return area
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.delete("/area/{area_id}", response_model=dict, tags=["Area"])
async def delete_area(area_id: int, session: AsyncSession = Depends(get_session)):
    try:
        area_use_case = AreaUseCaseFactory(session).build()
        result = await area_use_case.delete_area(area_id)

        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/area/name/{area_id}", response_model=Optional[str], tags=["Area"])
async def get_area_name_by_id(area_id: int, session: AsyncSession = Depends(get_session)):
    try:
        area_use_case = AreaUseCaseFactory(session).build()
        area_name = await area_use_case.get_area_name_by_id(area_id)

        return area_name
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")