from app.application.ports.filter_match_port import FilterMatchPort
from app.domain.services.filter_match_service import FilterMatchService
from app.domain.entities.job_offer import JobOffer
from typing import Dict, Any, List

class RunFilterMatchUseCase:
    def __init__(self, filter_match_port: FilterMatchPort, filter_match_service: FilterMatchService):
        self.filter_match_port = filter_match_port
        self.filter_match_service = filter_match_service

    async def preprocess_all_job_offers(self, job_offer_ids: List[int]) -> List[Dict[str, Any]]:
        result = await self.filter_match_port.preprocess_all_job_offers(job_offer_ids)
        return result

    async def preprocess_job_offer(self, job_offer_id: int) -> Dict[str, Any]:
        result = await self.filter_match_port.preprocess_job_offer(job_offer_id)
        if not result:
            raise ValueError("Error en el preprocesamiento de la oferta de trabajo")
        return result
    
    async def preprocess_all_students(self, student_ids: List[int]) -> List[Dict[str, Any]]:
        result = await self.filter_match_port.preprocess_all_students(student_ids)
        return result
    
    async def preprocess_student(self, student_id: int) -> Dict[str, Any]:
        result = await self.filter_match_port.preprocess_student(student_id)
        if not result:
            raise ValueError("Error en el preprocesamiento del estudiante")
        return result