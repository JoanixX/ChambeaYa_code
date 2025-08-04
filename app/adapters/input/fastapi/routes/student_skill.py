from typing import List
import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session

from app.domain.entities.student_skill import StudentSkill
from app.adapters.input.fastapi.schemas.student_skill_schema import (StudentSkillResponse, StudentSkillCreate)
from app.application.factories.student_skill_factory import StudentSkillUseCaseFactory

router = APIRouter()
# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/student/student_skill", response_model=StudentSkillResponse, tags=["Student", "Skill"])
async def add_student_skill(request: Request, student_skill: StudentSkillCreate, session: AsyncSession = Depends(get_session)):
    try:
        student_skill_use_case = StudentSkillUseCaseFactory(session).build()

        student_skill  = StudentSkill(
            student_id=student_skill.student_id,
            skill_id=student_skill.skill_id
        )

        result = await student_skill_use_case.add_student_skill(student_skill)
        return StudentSkillResponse(student_id=result.student_id, skill_id=result.skill_id)
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error al agregar skills al estudiante: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/student/{student_id}/skills", response_model=List[StudentSkillResponse], tags=["Student", "Skill"])
async def get_student_skills(student_id: int, session: AsyncSession = Depends(get_session)):
    try:
        student_skill_use_case = StudentSkillUseCaseFactory(session).build()

        skills = await student_skill_use_case.get_student_skills(student_id)
        return [
            {
                "student_id": skill.student_id,
                "skill_id": skill.skill_id
            }
            for skill in skills
        ]
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
@router.delete("/student/{student_id}/skill/{skill_id}", response_model=dict, tags=["Student", "Skill"])
async def delete_student_skill(student_id: int, skill_id: int, session: AsyncSession = Depends(get_session)):
    try:
        student_skill_use_case = StudentSkillUseCaseFactory(session).build()
        deleted = await student_skill_use_case.delete_student_skill(student_id, skill_id)

        return deleted
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")