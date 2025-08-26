from typing import List
import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session

from app.domain.entities.company_area import CompanyArea
from app.adapters.input.fastapi.schemas.company_area_schema import (CompanyAreaResponse, CompanyAreaCreate)
from app.application.factories.company_area_factory import CompanyAreaUseCaseFactory

router = APIRouter()
# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
    
@router.post("/company/company_area", response_model=CompanyAreaResponse, tags=["Company", "Area"])
async def add_company_area(request: Request, company_area: CompanyAreaCreate, session: AsyncSession = Depends(get_session)):
    try:
        company_area_use_case = CompanyAreaUseCaseFactory(session).build()

        company_area  = CompanyArea(
            company_id=company_area.company_id,
            area_id=company_area.area_id
        )

        result = await company_area_use_case.add_company_area(company_area)
        return CompanyAreaResponse(company_id=result.company_id, area_id=result.area_id)
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error al agregar area a la compañia: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/company/{company_id}/areas", response_model=List[CompanyAreaResponse], tags=["Company", "Area"])
async def get_company_areas(company_id: int, session: AsyncSession = Depends(get_session)):
    try:
        company_area_use_case = CompanyAreaUseCaseFactory(session).build()

        areas = await company_area_use_case.get_company_areas(company_id)
        return [area.__dict__ for area in areas]
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
@router.delete("/company/{company_id}/area/{area_id}", response_model=dict, tags=["Company", "Area"])
async def delete_company_area(company_id: int, area_id: int, session: AsyncSession = Depends(get_session)):
    try:
        company_area_use_case = CompanyAreaUseCaseFactory(session).build()
        deleted = await company_area_use_case.delete_company_area(company_id, area_id)

        return deleted
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")