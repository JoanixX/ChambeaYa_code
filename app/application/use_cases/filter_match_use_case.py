from app.application.ports.filter_match_port import FilterMatchPort
from app.domain.entities.job_offer import JobOffer

class RunFilterMatchUseCase:
    def __init__(self, filter_match_port: FilterMatchPort):
        self.filter_match_port = filter_match_port

    async def preprocess_job_offer(self, job_offer: JobOffer):
        result = await self.filter_match_port.preprocess_job_offer(job_offer)
        return result
    
    async def preprocess_all_job_offers(self, job_offers: list[JobOffer]):
        result = await self.filter_match_port.preprocess_all_job_offers(job_offers)
        return result
    
    async def preprocess_student(self, student_id: int):
        result = await self.filter_match_port.preprocess_student(student_id)
        return result
    
    async def preprocess_all_students(self, student_ids: list[int]):
        result = await self.filter_match_port.preprocess_all_students(student_ids)
        return result