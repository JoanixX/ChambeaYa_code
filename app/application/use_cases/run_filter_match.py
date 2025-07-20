from app.application.ports.run_filter_match_port import RunFilterMatchPort
from app.domain.entities.job_offer import JobOffer

class RunFilterMatchUseCase:
    def __init__(self, filter_match_port: RunFilterMatchPort):
        self.filter_match_port = filter_match_port

    async def execute(self, job_offer: JobOffer):
        result = await self.filter_match_port.preprocess_job_offer(job_offer)
        return result