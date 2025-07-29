from app.infraestructure.ai_client.ai_connection import preprocess_all_job_offers
from app.infraestructure.ai_client.ai_connection import preprocess_job_offer
from app.adapters.output.orm.repositories.job_offer_required_skill_repository_impl import JobOfferRequiredSkillRepositoryImpl
from app.adapters.output.orm.repositories.skill_repository_impl import get_skill_by_id_impl
from app.domain.entities.job_offer import JobOffer
from typing import List

class PreprocessJobOfferService:
    async def preprocess_all(self, job_offers: List[JobOffer], session):
        job_offers_data = []
        job_offer_skill_repo = JobOfferRequiredSkillRepositoryImpl(session)

        for j in job_offers:
            skill_links = await job_offer_skill_repo.get_by_job_offer_id(j.id)

            skill_names = []
            for link in skill_links:
                skill = await get_skill_by_id_impl(session, link.skill_id)
                if skill:
                    skill_names.append(skill.name)
        
        print("=== DATA ENVIADA A IA ===")
        from pprint import pprint
        pprint(job_offers_data)


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
                "required_skills": skill_names,
                "embedding": None
            })
        return await preprocess_all_job_offers(job_offers_data)

    async def preprocess_job_offer(self, job_offer: JobOffer):
        job_offer_data = {
            "id": job_offer.id,
            "title": job_offer.title,
            "description": job_offer.description,
            "required_hours": job_offer.required_hours,
            "approximated_salary": job_offer.approximated_salary,
            "duration": job_offer.duration,
            "start_date": job_offer.start_date.isoformat() if job_offer.start_date else None,
            "area_id": job_offer.area_id,
            "experience_id": job_offer.experience_id,
            "modality": job_offer.modality,
            "required_skills": [],
            "embedding": None
        }
        return await preprocess_job_offer(job_offer_data)