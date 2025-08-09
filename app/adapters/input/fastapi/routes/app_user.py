from typing import List
import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session

from app.application.factories.app_user_factory import AppUserUseCaseFactory
from app.adapters.input.fastapi.schemas.app_user_schema import AppUserCreate, AppUserResponse, LoginCreate

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/register/user", response_model=AppUserResponse, tags=["App User"])
async def register_user(request: Request, app_user: AppUserCreate, session: AsyncSession = Depends(get_session)):
    try:
        body = await request.body()
        logger.info(f"Body recibido: {body.decode()}")
        logger.info(f"Iniciando registro de usuario: {app_user.email}")
        
        app_user_use_case = AppUserUseCaseFactory(session).build()

        logger.info("Ejecutando caso de uso...")
        result = await app_user_use_case.register_user(app_user.dict())
        
        logger.info(f"Usuario registrado exitosamente: {result}")
        return JSONResponse(content=result)
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error interno del servidor: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    

@router.get("/user/{app_user_email}", response_model=AppUserResponse, tags=["App User"])
async def get_user_by_email(app_user_email: str, session: AsyncSession = Depends(get_session)):
    try:
        app_user_use_case = AppUserUseCaseFactory(session).build()
        app_user = await app_user_use_case.get_user_by_email(app_user_email)
        user_dict = app_user.__dict__.copy()
        if hasattr(app_user, 'role') and hasattr(app_user.role, 'value'):
            user_dict['role'] = app_user.role.value
        return user_dict
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.post("/login", tags=["App User"])
async def login(credentials: LoginCreate, session: AsyncSession = Depends(get_session)):
    app_user_use_case = AppUserUseCaseFactory(session).build()
    try:
        result = await app_user_use_case.login(credentials.email, credentials.password, session)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error interno del servidor: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")