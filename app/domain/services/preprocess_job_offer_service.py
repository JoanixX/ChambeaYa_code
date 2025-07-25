from app.infraestructure.ai_client.ai_connection import preprocess_all_job_offers
from app.domain.entities.job_offer import JobOffer
from typing import List

class PreprocessJobOfferService:
    async def preprocess_all(self, job_offers: List[JobOffer]):
        job_offers_data = []
        for j in job_offers:
            job_offers_data.append({
                "id": j.id,
                "title": j.title,
                "description": j.description,
                "required_hours": j.required_hours,
                "approximated_salary": j.approximated_salary,
                "duration": j.duration,
                "start_date": j.start_date.isoformat() if j.start_date else None,
                "area_id": j.area_id,
                "experience_id": j.experience_id,
                "modality": j.modality,
                "required_skills": [],
                "embedding": None
            })
        return await preprocess_all_job_offers(job_offers_data)
