from typing import List
import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session

from app.adapters.input.fastapi.schemas.chat_history_schema import (ChatHistoryCreate, ChatHistoryResponse)
from app.application.factories.chat_history_factory import ChatHistoryUseCaseFactory

router = APIRouter()
# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/register/chat_history", response_model=dict, tags=["Chat History"])
async def register_chat_history(request: Request, chat_history: ChatHistoryCreate, session: AsyncSession = Depends(get_session)):
    try:
        body = await request.body()
        logger.info(f"Datos recibidos para registrar historial de chat: {body.decode()}")
        logger.info(f"Iniciando registro del historial de chat: {chat_history.message}")

        chat_history_use_case = ChatHistoryUseCaseFactory(session).build()
        
        logger.info("Ejecutando caso de uso...")
        result = await chat_history_use_case.register_chat_history(chat_history.dict())
        logger.info(f"Historial de chat registrado exitosamente: {result}")
        return JSONResponse(content=result)
    
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error al registrar el historial de chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/chat_history/{chat_history_phone_number}", response_model=dict, tags=["Chat History"])
async def get_chat_history_by_phone_number(chat_history_phone_number: str, session: AsyncSession = Depends(get_session)):
    try:
        chat_history_use_case = ChatHistoryUseCaseFactory(session).build()
        chat_history = await chat_history_use_case.get_chat_history(chat_history_phone_number)
        return ChatHistoryResponse(**chat_history.__dict__).model_dump()
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error al obtener la empresa: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.delete("/chat_history/{chat_history_phone_number}", response_model=dict, tags=["Chat History"])
async def delete_chat_history(chat_history_phone_number: str, session: AsyncSession = Depends(get_session)):
    try:
        chat_history_use_case = ChatHistoryUseCaseFactory(session).build()
        deleted_chat_history = await chat_history_use_case.delete_chat_history(chat_history_phone_number)
        return deleted_chat_history
    
    except ValueError as e: 
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error al eliminar la empresa: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")