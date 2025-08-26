from typing import List, Dict
import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session

from app.adapters.input.fastapi.schemas.external_link_schema import (ExternalLinkCreate, ExternalLinkResponse)
from app.application.factories.external_link_factory import ExternalLinkUseCaseFactory

router = APIRouter()
# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/register/external_link", response_model=dict, tags=["External Link"])
async def register_external_link(request: Request, external_link: ExternalLinkCreate , session: AsyncSession = Depends(get_session)):
    try:
        body = await request.body()
        logger.info(f"Body recibido: {body.decode()}")
        logger.info(f"Iniciando registro de link: {external_link.name}")

        external_link_use_case = ExternalLinkUseCaseFactory(session).build()

        logger.info("Ejecutando caso de uso...")
        result = await external_link_use_case.register_external_link(external_link.dict())
        logger.info(f"Link registrado con éxito: {result}")
        return JSONResponse(content=result)
    
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error al registrar link: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.post("/external_link/all", response_model=List[dict], tags=["External Link"])
async def get_all_external_links(session: AsyncSession = Depends(get_session)):
    try:
        external_link_use_case = ExternalLinkUseCaseFactory(session).build()
        external_links = await external_link_use_case.get_all_external_links()
        return [ExternalLinkResponse(**el.__dict__).model_dump() for el in external_links]
    
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/external_link/{external_link_id}", response_model=dict, tags=["External Link"])
async def get_external_link(external_link_id: int, session: AsyncSession = Depends(get_session)):
    try:
        external_link_use_case = ExternalLinkUseCaseFactory(session).build()
        external_link = await external_link_use_case.get_external_link(external_link_id)
        return ExternalLinkResponse(**external_link.__dict__).model_dump()
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/student/{student_id}/external_links", response_model=List[Dict], tags=["External Link", "Student"])
async def get_student_external_links(student_id: int, session: AsyncSession = Depends(get_session)):
    try:
        external_link_use_case = ExternalLinkUseCaseFactory(session).build()
        external_links = await external_link_use_case.get_student_external_links(student_id)
        return [ExternalLinkResponse(**el.__dict__).model_dump() for el in external_links]
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
@router.put("/external_link/{external_link_id}", response_model=dict, tags=["External Link"])
async def update_external_link(external_link_id: int, external_link: ExternalLinkCreate, session: AsyncSession = Depends(get_session)):
    try:
        external_link_use_case = ExternalLinkUseCaseFactory(session).build()
        updated = await external_link_use_case.update_external_link(external_link_id, external_link.dict())
        return ExternalLinkResponse(**updated.__dict__).model_dump()
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
@router.delete("/external_link/{external_link_id}", response_model=dict, tags=["External Link"])
async def delete_external_link(external_link_id: int, session: AsyncSession = Depends(get_session)):
    try:
        external_link_use_case = ExternalLinkUseCaseFactory(session).build()
        deleted = await external_link_use_case.delete_external_link(external_link_id)
        return deleted
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")