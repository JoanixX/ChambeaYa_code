from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session
from app.domain.entities.job_offer_required_skill import JobOfferRequiredSkill
from app.application.use_cases.job_offer_required_skill_use_case import JobOfferRequiredSkillUseCase
from app.adapters.output.orm.repositories.job_offer_required_skill_repository_impl import JobOfferRequiredSkillRepositoryImpl
from app.domain.services.job_offer_required_skill_service import JobOfferRequiredSkillService
from app.application.ports.job_offer_required_skill_port import JobOfferRequiredSkillPort
from pydantic import BaseModel

router = APIRouter()

class JobOfferRequiredSkillPortImpl(JobOfferRequiredSkillPort):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = JobOfferRequiredSkillRepositoryImpl(session)

    async def get_skills_for_job_offer(self, job_offer_id: int):
        return await self.repository.get_by_job_offer_id(job_offer_id)

    async def add_required_skill(self, job_offer_required_skill: JobOfferRequiredSkill):
        return await self.repository.add(job_offer_required_skill)

    async def remove_required_skill(self, job_offer_required_skill_id: int):
        await self.repository.remove(job_offer_required_skill_id)

class JobOfferRequiredSkillCreate(BaseModel):
    job_offer_id: int
    skill_id: int

@router.post("/job_offer/required_skill", response_model=dict, tags=["Job Offer Required Skill"])
async def add_required_skill(skill: JobOfferRequiredSkillCreate, session: AsyncSession = Depends(get_session)):
    port = JobOfferRequiredSkillPortImpl(session)
    service = JobOfferRequiredSkillService(port)
    use_case = JobOfferRequiredSkillUseCase(port, service)
    skill_entity = JobOfferRequiredSkill(skill.job_offer_id, skill.skill_id)
    result = await use_case.add_required_skill(skill_entity)
    return JSONResponse(content=result.__dict__)

@router.delete("/job_offer/required_skill/{required_skill_id}", tags=["Job Offer Required Skill"])
async def remove_required_skill(required_skill_id: int, session: AsyncSession = Depends(get_session)):
    try:
        port = JobOfferRequiredSkillPortImpl(session)
        service = JobOfferRequiredSkillService(port)
        use_case = JobOfferRequiredSkillUseCase(port, service)
        await use_case.remove_required_skill(required_skill_id)
        return JSONResponse(content={"message": "Required skill removed"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")