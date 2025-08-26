from typing import List
import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session

from app.adapters.input.fastapi.schemas.company_schema import (CompanyCreate, CompanyResponse)
from app.application.factories.company_factory import CompanyUseCaseFactory

router = APIRouter()
# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/register/company", response_model=dict, tags=["Company"])
async def register_company(request: Request, company: CompanyCreate, session: AsyncSession = Depends(get_session)):
    try:
        body = await request.body()
        logger.info(f"Datos recibidos para registrar empresa: {body.decode()}")
        logger.info(f"Iniciando registro de la empresa: {company.name}")

        company_use_case = CompanyUseCaseFactory(session).build()
        
        logger.info("Ejecutando caso de uso...")
        result = await company_use_case.register_company(company.dict())
        logger.info(f"Empresa registrada exitosamente: {result}")
        return JSONResponse(content=result)
    
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error al registrar la empresa: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/company/all", response_model=List[dict], tags=["Company"])
async def get_all_companies(session: AsyncSession = Depends(get_session)):
    try:
        company_use_case = CompanyUseCaseFactory(session).build()
        companies = await company_use_case.get_all_companies()
        return [CompanyResponse(**c.__dict__).model_dump() for c in companies]
    
    except Exception as e:
        logger.error(f"Error al obtener empresas: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/company/{company_id}", response_model=dict, tags=["Company"])
async def get_company_by_id(company_id: int, session: AsyncSession = Depends(get_session)):
    try:
        company_use_case = CompanyUseCaseFactory(session).build()
        company = await company_use_case.get_company(company_id)
        return CompanyResponse(**company.__dict__).model_dump()
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error al obtener la empresa: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.put("/company/{company_id}", response_model=dict, tags=["Company"])
async def update_company(company_id: int, company: CompanyCreate, session: AsyncSession = Depends(get_session)):
    try:
        company_use_case = CompanyUseCaseFactory(session).build()
        updated_company = await company_use_case.update_company(company_id, company.dict())
        return CompanyResponse(**updated_company.__dict__).model_dump()
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error al actualizar la empresa: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.delete("/company/{company_id}", response_model=dict, tags=["Company"])
async def delete_company(company_id: int, session: AsyncSession = Depends(get_session)):
    try:
        company_use_case = CompanyUseCaseFactory(session).build()
        deleted_company = await company_use_case.delete_company(company_id)
        return deleted_company
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error al eliminar la empresa: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")