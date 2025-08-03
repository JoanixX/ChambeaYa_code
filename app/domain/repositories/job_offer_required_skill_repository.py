from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.job_offer_required_skill import JobOfferRequiredSkill

class JobOfferRequiredSkillRepository(ABC):
    @abstractmethod
    def get_by_job_offer_id(self, job_offer_id: int) -> List[JobOfferRequiredSkill]:
        pass

    @abstractmethod
    def exists(self, job_offer_id: int, skill_id: int) -> bool:
        pass

    @abstractmethod
    def save(self, job_offer_required_skill: JobOfferRequiredSkill) -> JobOfferRequiredSkill:
        pass

    @abstractmethod
    def delete(self, job_offer_required_skill_id: int) -> None:
        pass