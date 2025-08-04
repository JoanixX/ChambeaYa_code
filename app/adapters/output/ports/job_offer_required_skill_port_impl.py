from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.job_offer_required_skill import JobOfferRequiredSkill
from app.adapters.output.orm.repositories.job_offer_required_skill_repository_impl import JobOfferRequiredSkillRepositoryImpl
from app.application.ports.job_offer_required_skill_port import JobOfferRequiredSkillPort

class JobOfferRequiredSkillPortImpl(JobOfferRequiredSkillPort):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.job_offer_required_skill_repo = JobOfferRequiredSkillRepositoryImpl(session)

    async def add_job_offer_required_skill(self, job_offer_required_skill: JobOfferRequiredSkill) -> JobOfferRequiredSkill:
        return await self.job_offer_required_skill_repo.save(job_offer_required_skill)

    async def get_job_offer_required_skills(self, job_offer_id: int) -> List[JobOfferRequiredSkill]:
        return await self.job_offer_required_skill_repo.get_by_job_offer_id(job_offer_id)
    
    async def delete_job_offer_required_skill(self, job_offer_id: int, skill_id: int) -> bool:
        return await self.job_offer_required_skill_repo.delete(job_offer_id, skill_id)
    
    async def job_offer_required_skill_exists(self, job_offer_id: int, skill_id: int) -> bool:
        return await self.job_offer_required_skill_repo.exists(job_offer_id, skill_id)