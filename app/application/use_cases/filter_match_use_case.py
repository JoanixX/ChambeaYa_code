from app.application.ports.filter_match_port import FilterMatchPort
from app.domain.services.filter_match_service import FilterMatchService
from app.domain.entities.filter_match import FilterMatch
from typing import List

class FilterMatchUseCase:
    def __init__(self, filter_match_port: FilterMatchPort, filter_match_service: FilterMatchService):
        self.filter_match_port = filter_match_port
        self.filter_match_service = filter_match_service

    async def preprocess_all_job_offers(self, job_offer_ids: List[int]) -> List[dict]:
        result = await self.filter_match_service.preprocess_all_job_offers(job_offer_ids)
        # Devuelve lista vacía si no hay resultados válidos
        return result or []

    async def preprocess_job_offer(self, job_offer_id: int) -> dict:
        result = await self.filter_match_service.preprocess_job_offer(job_offer_id)
        if not result:
            raise ValueError("Error en el preprocesamiento de la oferta de trabajo")
        return result

    async def preprocess_all_students(self, student_ids: List[int]) -> List[dict]:
        result = await self.filter_match_service.preprocess_all_students(student_ids)
        return result or []

    async def preprocess_student(self, student_id: int) -> dict:
        result = await self.filter_match_service.preprocess_student(student_id)
        if not result:
            raise ValueError("Error en el preprocesamiento del estudiante")
        return result