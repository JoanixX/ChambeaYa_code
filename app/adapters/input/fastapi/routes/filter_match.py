from fastapi import APIRouter
from app.application.use_cases.run_filter_match import RunFilterMatchUseCase
from app.application.ports.run_filter_match_port import RunFilterMatchPort
from app.infraestructure.ai_client.ai_connection import call_filter_match_ia

router = APIRouter()

class FilterMatchPortAdapter(RunFilterMatchPort):
    async def preprocess_job_offer(self, job_offer):
        return call_filter_match_ia(job_offer)

@router.post("/filter-match/")
async def create_filter_match(job_offer: dict):
    port = FilterMatchPortAdapter()
    use_case = RunFilterMatchUseCase(port)
    result = await use_case.execute(job_offer)
    return result