from app.domain.entities.job_offer_required_skill import JobOfferRequiredSkill
from app.domain.repositories.job_offer_required_skill_repository import JobOfferRequiredSkillRepository
from typing import List

class JobOfferRequiredSkillService:
    def __init__(self, job_offer_required_skill_repo: JobOfferRequiredSkillRepository):
        self.job_offer_required_skill_repo = job_offer_required_skill_repo

    async def add_job_offer_required_skill(self, job_offer_required_skill: JobOfferRequiredSkill) -> JobOfferRequiredSkill:
        exists = await self.job_offer_required_skill_repo.exists(
            job_offer_required_skill.job_offer_id, job_offer_required_skill.skill_id
        )

        if exists:
            raise ValueError("La oferta de trabajo ya tiene esta skill requerida")

        saved_model = await self.job_offer_required_skill_repo.save(job_offer_required_skill)

        if saved_model:
            return saved_model
        else:
            raise ValueError("Error al guardar la skill requerida de la oferta de trabajo")

    async def get_job_offer_required_skills(self, job_offer_id: int) -> List[JobOfferRequiredSkill]:
        return await self.job_offer_required_skill_repo.get_by_job_offer_id(job_offer_id)

    async def delete_job_offer_required_skill(self, job_offer_id: int, skill_id: int) -> bool:
        return await self.job_offer_required_skill_repo.delete(job_offer_id, skill_id)