from typing import List, Optional
from app.domain.entities.job_offer_required_skill import JobOfferRequiredSkill
from app.domain.repositories.job_offer_required_skill_repository import JobOfferRequiredSkillRepository
from app.adapters.output.orm.models.job_offer_required_skill_model import JobOfferRequiredSkillModel
from sqlalchemy.future import select

class JobOfferRequiredSkillRepositoryImpl(JobOfferRequiredSkillRepository):
    def __init__(self, session):
        self.session = session

    async def get_by_job_offer_id(self, job_offer_id: int) -> List[JobOfferRequiredSkill]:
        result = await self.session.execute(select(JobOfferRequiredSkillModel).where(JobOfferRequiredSkillModel.job_offer_id == job_offer_id))
        models = result.scalars().all()
        return [JobOfferRequiredSkill(job_offer_id=m.job_offer_id, skill_id=m.skill_id) for m in models]

    async def add(self, job_offer_required_skill: JobOfferRequiredSkill) -> JobOfferRequiredSkill:
        model = JobOfferRequiredSkillModel(job_offer_id=job_offer_required_skill.job_offer_id, skill_id=job_offer_required_skill.skill_id)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return JobOfferRequiredSkill(job_offer_id=model.job_offer_id, skill_id=model.skill_id)

    async def remove(self, job_offer_required_skill_id: int) -> None:
        await self.session.execute(
            JobOfferRequiredSkillModel.__table__.delete().where(JobOfferRequiredSkillModel.id == job_offer_required_skill_id)
        )
        await self.session.commit()
