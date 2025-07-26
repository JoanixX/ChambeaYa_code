from typing import List
from app.domain.entities.job_offer_required_skill import JobOfferRequiredSkill
from app.domain.services.job_offer_required_skill_service import JobOfferRequiredSkillService
from app.application.ports.job_offer_required_skill_port import JobOfferRequiredSkillPort

class JobOfferRequiredSkillUseCase:
    def __init__(self, port: JobOfferRequiredSkillPort, service: JobOfferRequiredSkillService):
        self.port = port
        self.service = service

    async def get_skills_for_job_offer(self, job_offer_id: int) -> List[JobOfferRequiredSkill]:
        return await self.service.get_skills_for_job_offer(job_offer_id)

    async def add_required_skill(self, job_offer_required_skill: JobOfferRequiredSkill) -> JobOfferRequiredSkill:
        return await self.service.add_required_skill(job_offer_required_skill)

    async def remove_required_skill(self, job_offer_required_skill_id: int) -> None:
        await self.service.remove_required_skill(job_offer_required_skill_id)
