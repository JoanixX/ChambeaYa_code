from typing import List, Optional
from sqlalchemy.future import select
from sqlalchemy import delete
from app.domain.entities.job_offer_required_skill import JobOfferRequiredSkill
from app.domain.repositories.job_offer_required_skill_repository import JobOfferRequiredSkillRepository
from app.adapters.output.orm.models.job_offer_required_skill_model import JobOfferRequiredSkillModel

class JobOfferRequiredSkillRepositoryImpl(JobOfferRequiredSkillRepository):
    def __init__(self, session):
        self.session = session

    async def get_by_job_offer_id(self, job_offer_id: int) -> List[JobOfferRequiredSkill]:
        result = await self.session.execute(
            select(JobOfferRequiredSkillModel).where(JobOfferRequiredSkillModel.job_offer_id == job_offer_id)
        )
        models = result.scalars().all()
        skills = []
        for model in models:
            skills.append(
                JobOfferRequiredSkill(
                    job_offer_id=model.job_offer_id, 
                    skill_id=model.skill_id
                )
            )
        return skills

    async def exists(self, job_offer_id: int, skill_id: int) -> bool:
        result = await self.session.execute(
            select(JobOfferRequiredSkillModel).where(
                JobOfferRequiredSkillModel.job_offer_id == job_offer_id,
                JobOfferRequiredSkillModel.skill_id == skill_id
            )
        )
        return result.scalar_one_or_none() is not None

    async def save(self, job_offer_required_skill: JobOfferRequiredSkill) -> JobOfferRequiredSkill:
        exists = await self.exists(job_offer_required_skill.job_offer_id, 
                                   job_offer_required_skill.skill_id)
        if exists:
            return job_offer_required_skill
        
        model = JobOfferRequiredSkillModel(
            job_offer_id=job_offer_required_skill.job_offer_id,
            skill_id=job_offer_required_skill.skill_id
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return JobOfferRequiredSkill(job_offer_id=model.job_offer_id, skill_id=model.skill_id)

    async def delete(self, job_offer_id: int, skill_id: int) -> bool:
        result = await self.session.execute(
            select(JobOfferRequiredSkillModel).where(
                JobOfferRequiredSkillModel.job_offer_id == job_offer_id,
                JobOfferRequiredSkillModel.skill_id == skill_id
            )
        )
        model = result.scalar_one_or_none()
        if not model:
            return False

        await self.session.execute(
            delete(JobOfferRequiredSkillModel).where(
                JobOfferRequiredSkillModel.job_offer_id == job_offer_id,
                JobOfferRequiredSkillModel.skill_id == skill_id
            )
        )
        await self.session.commit()
        return True