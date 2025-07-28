from typing import List
from app.domain.entities.job_offer_required_skill import JobOfferRequiredSkill
from app.application.ports.job_offer_required_skill_port import JobOfferRequiredSkillPort

class JobOfferRequiredSkillService:
    def __init__(self, port: JobOfferRequiredSkillPort):
        self.port = port

    async def get_skills_for_job_offer(self, job_offer_id: int) -> List[JobOfferRequiredSkill]:
        return await self.port.get_skills_for_job_offer(job_offer_id)

    async def add_required_skill(self, job_offer_required_skill: JobOfferRequiredSkill) -> JobOfferRequiredSkill:
        return await self.port.add_required_skill(job_offer_required_skill)

    async def remove_required_skill(self, job_offer_required_skill_id: int) -> None:
        await self.port.remove_required_skill(job_offer_required_skill_id)