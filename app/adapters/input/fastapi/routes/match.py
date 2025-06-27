from fastapi import APIRouter, Body
from app.application.use_cases.create_match import CreateMatchUseCase
from app.application.ports.create_match_port import CreateMatchPort
from app.infraestructure.ai_client.ai_connection import call_match_job_student_ia

router = APIRouter()

class CreateMatchPortAdapter(CreateMatchPort):
    async def call_ai_service(self, estudiante, job_offer):
        return call_match_job_student_ia(estudiante, job_offer)

@router.post("/match/")
async def create_match(estudiante: dict = Body(...), job_offer: dict = Body(...)):
    port = CreateMatchPort()
    use_case = CreateMatchUseCase(port)
    result = use_case.execute(estudiante, job_offer)
    return result