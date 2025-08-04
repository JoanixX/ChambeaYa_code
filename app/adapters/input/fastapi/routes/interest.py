from typing import List, Optional
import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session

from app.adapters.input.fastapi.schemas.interest_schema import (InterestCreate, InterestResponse)
from app.application.factories.interest_factory import InterestUseCaseFactory

router = APIRouter()
# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/register/interest", response_model=InterestResponse, tags=["Interest"])
async def register_interest(request: Request, interest: InterestCreate, session: AsyncSession = Depends(get_session)):
    try:
        body = await request.body()
        logger.info(f"Body recibido: {body.decode()}")
        logger.info(f"Iniciando registro de interest: {interest.name}")
        
        interest_use_case = InterestUseCaseFactory(session).build()

        logger.info("Ejecutando caso de uso...")
        interest_id = await interest_use_case.register_interest(interest.dict())
        interest_obj = await interest_use_case.get_interest(interest_id)
        
        logger.info(f"Interest registrado exitosamente: {interest_obj}")
        return interest_obj
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error interno del servidor: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/interest/all", response_model=List[InterestResponse], tags=["Interest"])
async def get_all_interests(session: AsyncSession = Depends(get_session)):
    try:
        interest_use_case = InterestUseCaseFactory(session).build()
        interests = await interest_use_case.get_all_interests()

        return interests
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/interest/{interest_id}", response_model=InterestResponse, tags=["Interest"])
async def get_interest_by_id(interest_id: int, session: AsyncSession = Depends(get_session)):
    try:
        interest_use_case = InterestUseCaseFactory(session).build()
        interest = await interest_use_case.get_interest(interest_id)

        return interest
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.delete("/interest/{interest_id}", response_model=dict, tags=["Interest"])
async def delete_interest(interest_id: int, session: AsyncSession = Depends(get_session)):
    try:
        interest_use_case = InterestUseCaseFactory(session).build()
        result = await interest_use_case.delete_interest(interest_id)

        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/interest/name/{interest_id}", response_model=Optional[str], tags=["Interest"])
async def get_interest_name_by_id(interest_id: int, session: AsyncSession = Depends(get_session)):
    try:
        interest_use_case = InterestUseCaseFactory(session).build()
        interest_name = await interest_use_case.get_interest_name_by_id(interest_id)

        return interest_name
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")