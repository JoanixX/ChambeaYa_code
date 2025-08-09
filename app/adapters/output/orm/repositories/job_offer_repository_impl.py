from sqlalchemy.future import select
from sqlalchemy import delete
from typing import Optional

from app.adapters.output.orm.models.job_offer_model import JobOfferModel
from app.domain.entities.job_offer import JobOffer
from app.domain.repositories.job_offer_repository import JobOfferRepository
from app.adapters.output.orm.models.job_offer_required_skill_model import JobOfferRequiredSkillModel
from app.adapters.output.orm.models.skill_model import SkillModel
from app.adapters.output.orm.repositories.area_repository_impl import get_area_name_by_id_impl
from app.adapters.output.orm.repositories.experience_detail_repository_impl import get_experience_name_by_id_impl

class JobOfferRepositoryImpl(JobOfferRepository):
    def __init__(self, session):
        self.session = session

    async def get_enriched_job_offers(self, session) -> list:
        job_offers_result = await session.execute(select(JobOfferModel))
        job_offer_models = job_offers_result.scalars().all()
        enriched_job_offers = []
        for j in job_offer_models:
            area_id = None
            if j.area_id:
                area_id = await get_area_name_by_id_impl(session, j.area_id)

            experience_id = None
            if j.experience_id:
                experience_id = await get_experience_name_by_id_impl(session, j.experience_id)

            skill_links_result = await session.execute(
                select(JobOfferRequiredSkillModel).where(JobOfferRequiredSkillModel.job_offer_id == j.id))
            skill_links = skill_links_result.scalars().all()
            skills = []
            for link in skill_links:
                skill_result = await session.execute(select(SkillModel).where(SkillModel.id == link.skill_id))
                skill_obj = skill_result.scalar_one_or_none()
                if skill_obj:
                    skills.append({"name": skill_obj.name})

            enriched_job_offers.append({
                "id": j.id,
                "company_id": j.company_id,
                "title": j.title,
                "description": j.description,
                "required_hours": j.required_hours,
                "approximated_salary": j.approximated_salary,
                "duration": j.duration,
                "start_date": j.start_date.isoformat() if j.start_date else None,
                "area_id": area_id,
                "experience_id": experience_id,
                "required_skills": skills,
                "modality": j.modality,
                "embedding": j.embedding
            })
        return enriched_job_offers

    async def save(self, job_offer: JobOffer):
        model = JobOfferModel(
            company_id=job_offer.company_id,
            title=job_offer.title,
            description=job_offer.description,
            required_hours=job_offer.required_hours,
            approximated_salary=job_offer.approximated_salary,
            duration=job_offer.duration,
            start_date=job_offer.start_date,
            area_id=job_offer.area_id,
            experience_id=job_offer.experience_id,
            modality=job_offer.modality,
            embedding=job_offer.embedding
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def find_by_id(self, job_offer_id: int) -> Optional[JobOffer]:
        result = await self.session.execute(select(JobOfferModel).where(JobOfferModel.id == job_offer_id))
        model = result.scalar_one_or_none()
        if model:
            return JobOffer(
                id=model.id,
                company_id=model.company_id,
                title=model.title,
                description=model.description,
                required_hours=model.required_hours,
                approximated_salary=model.approximated_salary,
                duration=model.duration,
                start_date=model.start_date,
                area_id=model.area_id,
                experience_id=model.experience_id,
                modality=model.modality,
                embedding=model.embedding,
                created_at=model.created_at,
                updated_at=model.updated_at,
                deleted_at=model.deleted_at
            )
        return None

    async def find_by_company_id(self, company_id: int) -> list[JobOffer]:
        result = await self.session.execute(select(JobOfferModel).where(JobOfferModel.company_id == company_id))
        models = result.scalars().all()
        job_offers = []
        for model in models:
            job_offers.append(JobOffer(
                id=model.id,
                company_id=model.company_id,
                title=model.title,
                description=model.description,
                required_hours=model.required_hours,
                approximated_salary=model.approximated_salary,
                duration=model.duration,
                start_date=model.start_date,
                area_id=model.area_id,
                experience_id=model.experience_id,
                modality=model.modality,
                embedding=model.embedding,
                created_at=model.created_at,
                updated_at=model.updated_at,
                deleted_at=model.deleted_at
            ))
        return job_offers

    async def get_all(self) -> list[JobOffer]:
        result = await self.session.execute(select(JobOfferModel))
        models = result.scalars().all()
        job_offers = []
        for model in models:
            job_offers.append(
                JobOffer(
                    id=model.id,
                    company_id=model.company_id,
                    title=model.title,
                    description=model.description,
                    required_hours=model.required_hours,
                    approximated_salary=model.approximated_salary,
                    duration=model.duration,
                    start_date=model.start_date,
                    area_id=model.area_id,
                    experience_id=model.experience_id,
                    modality=model.modality,
                    embedding=model.embedding,
                    created_at=model.created_at,
                    updated_at=model.updated_at,
                    deleted_at=model.deleted_at
                )
            )
        return job_offers
    
    async def update(self, job_offer: JobOffer) -> Optional[JobOffer]:
        result = await self.session.execute(select(JobOfferModel).where(JobOfferModel.id == job_offer.id))
        model = result.scalar_one_or_none()
        if model:
            model.company_id = job_offer.company_id
            model.title = job_offer.title
            model.description = job_offer.description
            model.required_hours = job_offer.required_hours
            model.approximated_salary = job_offer.approximated_salary
            model.duration = job_offer.duration
            model.start_date = job_offer.start_date
            model.area_id = job_offer.area_id
            model.experience_id = job_offer.experience_id
            model.modality = job_offer.modality
            model.embedding = job_offer.embedding
            await self.session.commit()
            await self.session.refresh(model)
            return job_offer
        return None

    async def delete(self, job_offer_id: int):
        result = await self.session.execute(select(JobOfferModel).where(JobOfferModel.id == job_offer_id))
        model = result.scalar_one_or_none()
        if not model:
            return False
        
        await self.session.execute(delete(JobOfferModel).where(JobOfferModel.id == job_offer_id))
        await self.session.commit()
        return True