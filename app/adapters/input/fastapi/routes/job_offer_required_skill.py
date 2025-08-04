from typing import List
import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session

from app.domain.entities.job_offer_required_skill import JobOfferRequiredSkill
from app.adapters.input.fastapi.schemas.job_offer_required_skill_schema import (JobOfferRequiredSkillResponse, JobOfferRequiredSkillCreate)
from app.application.factories.job_offer_required_skill_factory import JobOfferRequiredSkillUseCaseFactory

router = APIRouter()
# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/job_offer/job_offer_required_skill", response_model=JobOfferRequiredSkillResponse, tags=["Job Offer", "Skill"])
async def add_job_offer_required_skill(
    request: Request, job_offer_required_skill: JobOfferRequiredSkillCreate, session: AsyncSession = Depends(get_session)):
    try:
        job_offer_required_skill_use_case = JobOfferRequiredSkillUseCaseFactory(session).build()

        job_offer_required_skill = JobOfferRequiredSkill(
            job_offer_id=job_offer_required_skill.job_offer_id,
            skill_id=job_offer_required_skill.skill_id
        )

        result = await job_offer_required_skill_use_case.add_job_offer_required_skill(job_offer_required_skill)
        return JobOfferRequiredSkillResponse(job_offer_id=result.job_offer_id, skill_id=result.skill_id)
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error al agregar skills al estudiante: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/job_offer/{job_offer_id}/skills", response_model=List[JobOfferRequiredSkillResponse], tags=["Job Offer", "Skill"])
async def get_job_offer_required_skills(job_offer_id: int, session: AsyncSession = Depends(get_session)):
    try:
        job_offer_required_skill_use_case = JobOfferRequiredSkillUseCaseFactory(session).build()

        skills = await job_offer_required_skill_use_case.get_job_offer_required_skills(job_offer_id)
        return [skill.__dict__ for skill in skills]
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
@router.delete("/job_offer/{job_offer_id}/skill/{skill_id}", response_model=dict, tags=["Job Offer", "Skill"])
async def delete_job_offer_required_skill(job_offer_id: int, skill_id: int, session: AsyncSession = Depends(get_session)):
    try:
        job_offer_required_skill_use_case = JobOfferRequiredSkillUseCaseFactory(session).build()
        deleted = await job_offer_required_skill_use_case.delete_job_offer_required_skill(job_offer_id, skill_id)

        return deleted
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")