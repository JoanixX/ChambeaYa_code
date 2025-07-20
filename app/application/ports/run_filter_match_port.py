from abc import ABC, abstractmethod
from app.domain.entities.job_offer import JobOffer

class RunFilterMatchPort(ABC):
    @abstractmethod
    async def preprocess_job_offer(self, job_offer: JobOffer):
        pass