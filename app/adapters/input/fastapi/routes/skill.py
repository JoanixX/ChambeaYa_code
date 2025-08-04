from typing import List, Optional
import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session

from app.adapters.input.fastapi.schemas.skill_schema import (SkillCreate, SkillResponse)
from app.application.factories.skill_factory import SkillUseCaseFactory

router = APIRouter()
# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/register/skill", response_model=SkillResponse, tags=["Skill"])
async def register_skill(request: Request, skill: SkillCreate, session: AsyncSession = Depends(get_session)):
    try:
        body = await request.body()
        logger.info(f"Body recibido: {body.decode()}")
        logger.info(f"Iniciando registro de skill: {skill.name}")
        
        skill_use_case = SkillUseCaseFactory(session).build()

        logger.info("Ejecutando caso de uso...")
        skill_id = await skill_use_case.register_skill(skill.dict())
        skill_obj = await skill_use_case.get_skill(skill_id)
        
        logger.info(f"Interest registrado exitosamente: {skill_obj}")
        return skill_obj
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error interno del servidor: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/skill/all", response_model=List[SkillResponse], tags=["Skill"])
async def get_all_skills(session: AsyncSession = Depends(get_session)):
    try:
        skill_use_case = SkillUseCaseFactory(session).build()
        students = await skill_use_case.get_all_skills()

        return students
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/skill/{skill_id}", response_model=SkillResponse, tags=["Skill"])
async def get_skill_by_id(skill_id: int, session: AsyncSession = Depends(get_session)):
    try:
        skill_use_case = SkillUseCaseFactory(session).build()
        skill = await skill_use_case.get_skill(skill_id)

        return skill
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.delete("/skill/{skill_id}", response_model=dict, tags=["Skill"])
async def delete_skill(skill_id: int, session: AsyncSession = Depends(get_session)):
    try:
        skill_use_case = SkillUseCaseFactory(session).build()
        result = await skill_use_case.delete_skill(skill_id)

        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
@router.get("/skill/name/{skill_id}", response_model=Optional[str], tags=["Skill"])
async def get_skill_name_by_id(skill_id: int, session: AsyncSession = Depends(get_session)):
    try:
        skill_use_case = SkillUseCaseFactory(session).build()
        skill_name = await skill_use_case.get_skill_name_by_id(skill_id)

        return skill_name
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")