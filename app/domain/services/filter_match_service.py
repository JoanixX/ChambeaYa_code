from typing import Dict, Any, List
from app.domain.repositories.filter_match_repository import FilterMatchRepository
from app.domain.entities.filter_match import FilterMatch
from app.infraestructure.ai_client.ai_connection import preprocess_job_offer, preprocess_student

class FilterMatchService:
    def __init__(self, filter_match_repo: FilterMatchRepository):
        self.filter_match_repo = filter_match_repo

    async def preprocess_all_job_offers(self, job_offer_service) -> List[Dict[str, Any]]:
        enriched_job_offers = await job_offer_service.get_enriched_job_offers()
        results = []
        for job_offer in enriched_job_offers:
            embedding_response = await preprocess_job_offer(job_offer)
            embedding = embedding_response.get("embedding")
            results.append({"job_offer_id": job_offer.id, "embedding": embedding})
        return results

    async def preprocess_all_students(self, student_service) -> List[Dict[str, Any]]:
        enriched_students = await student_service.get_enriched_students()
        results = []
        for student in enriched_students:
            student_dict = student.__dict__ if hasattr(student, "__dict__") else dict(student)
            embedding_response = await preprocess_student(student_dict)
            embedding = embedding_response.get("embedding")
            results.append({"student_id": student.id, "embedding": embedding})
        return results

    async def preprocess_job_offer(self, job_offer_service, job_offer_id) -> Dict[str, Any]:
        enriched_job_offers = await job_offer_service.get_enriched_job_offers()
        job_offer = next((jo for jo in enriched_job_offers if jo.id == job_offer_id), None)
        if not job_offer:
            return {"job_offer_id": job_offer_id, "embedding": None}
        embedding_response = await preprocess_job_offer(job_offer)
        embedding = embedding_response.get("embedding")
        return {"job_offer_id": job_offer_id, "embedding": embedding}

    async def preprocess_student(self, student_service, student_id) -> Dict[str, Any]:
        enriched_students = await student_service.get_enriched_students()
        student = next((st for st in enriched_students if st.id == student_id), None)
        if not student:
            return {"student_id": student_id, "embedding": None}
        embedding_response = await preprocess_student(student)
        embedding = embedding_response.get("embedding")
        return {"student_id": student_id, "embedding": embedding}
