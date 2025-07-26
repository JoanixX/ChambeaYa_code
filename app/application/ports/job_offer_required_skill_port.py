from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.job_offer_required_skill import JobOfferRequiredSkill

class JobOfferRequiredSkillPort(ABC):
    @abstractmethod
    async def get_skills_for_job_offer(self, job_offer_id: int) -> List[JobOfferRequiredSkill]:
        pass

    @abstractmethod
    async def add_required_skill(self, job_offer_required_skill: JobOfferRequiredSkill) -> JobOfferRequiredSkill:
        pass

    @abstractmethod
    async def remove_required_skill(self, job_offer_required_skill_id: int) -> None:
        pass
