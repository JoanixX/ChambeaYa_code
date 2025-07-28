from app.application.ports.filter_match_port import FilterMatchPort
from app.domain.entities.job_offer import JobOffer

class RunFilterMatchUseCase:
    def __init__(self, filter_match_port: FilterMatchPort):
        self.filter_match_port = filter_match_port

    async def execute(self, job_offer: JobOffer):
        result = await self.filter_match_port.preprocess_job_offer(job_offer)
        return result