from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.job_offer_required_skill import JobOfferRequiredSkill

class JobOfferRequiredSkillPort(ABC):
    @abstractmethod
    async def get_job_offer_required_skills(self, job_offer_id: int) -> List[JobOfferRequiredSkill]:
        pass

    @abstractmethod
    async def add_job_offer_required_skill(self, job_offer_required_skill: JobOfferRequiredSkill) -> JobOfferRequiredSkill:
        pass

    @abstractmethod
    async def delete_job_offer_required_skill(self, job_offer_id: int, skill_id: int) -> bool:
        pass