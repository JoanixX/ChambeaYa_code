from app.infraestructure.ai_client.ai_connection import preprocess_all_job_offers, preprocess_job_offer
from app.adapters.output.orm.repositories.job_offer_required_skill_repository_impl import JobOfferRequiredSkillRepositoryImpl
from app.adapters.output.orm.repositories.skill_repository_impl import get_skill_by_id_impl
from app.adapters.output.orm.repositories.area_repository_impl import get_area_name_by_id_impl
from app.adapters.output.orm.repositories.experience_detail_repository_impl import get_experience_name_by_id_impl
from app.domain.entities.job_offer import JobOffer
from typing import List

class PreprocessJobOfferService:
    async def preprocess_all(self, job_offers: List[JobOffer], session):
        job_offers_data = []
        job_offer_skill_repo = JobOfferRequiredSkillRepositoryImpl(session)
        for j in job_offers:
            # Fetch required skills as names
            skill_links = await job_offer_skill_repo.get_by_job_offer_id(j.id)
            skill_names = []
            for link in skill_links:
                skill = await get_skill_by_id_impl(session, link.skill_id)
                if skill:
                    skill_names.append(skill.name)
            # Fetch area as string
            area_name = await get_area_name_by_id_impl(session, j.area_id) if j.area_id else None
            # Fetch experience as string
            experience_name = await get_experience_name_by_id_impl(session, j.experience_id) if j.experience_id else None
            job_offers_data.append({
                "id": j.id,
                "title": j.title,
                "description": j.description,
                "area": area_name,
                "area_id": j.area_id,
                "experience": experience_name,
                "experience_id": j.experience_id,
                "required_skills": skill_names,
                "required_hours": j.required_hours,
                "approximated_salary": j.approximated_salary,
                "duration": j.duration,
                "start_date": j.start_date.isoformat() if j.start_date else None,
                "modality": j.modality,
                "embedding": None
            })
        print("[DEBUG] Payload sent to AI service (job_offers_data):", job_offers_data)
        return await preprocess_all_job_offers(job_offers_data)

    async def preprocess_job_offer(self, job_offer: JobOffer, session):
        job_offer_skill_repo = JobOfferRequiredSkillRepositoryImpl(session)
        # Fetch required skills as names
        skill_links = await job_offer_skill_repo.get_by_job_offer_id(job_offer.id)
        skill_names = []
        for link in skill_links:
            skill = await get_skill_by_id_impl(session, link.skill_id)
            if skill:
                skill_names.append(skill.name)
        # Fetch area as string
        area_name = await get_area_name_by_id_impl(session, job_offer.area_id) if job_offer.area_id else None
        # Fetch experience as string
        experience_name = await get_experience_name_by_id_impl(session, job_offer.experience_id) if job_offer.experience_id else None
        job_offer_data = {
            "id": job_offer.id,
            "title": job_offer.title,
            "description": job_offer.description,
            "area": area_name,
            "area_id": job_offer.area_id,
            "experience": experience_name,
            "experience_id": job_offer.experience_id,
            "required_skills": skill_names,
            "required_hours": job_offer.required_hours,
            "approximated_salary": job_offer.approximated_salary,
            "duration": job_offer.duration,
            "start_date": job_offer.start_date.isoformat() if job_offer.start_date else None,
            "modality": job_offer.modality,
            "embedding": None
        }
        print("[DEBUG] Payload sent to AI service (job_offer_data):", job_offer_data)
        return await preprocess_job_offer(job_offer_data)