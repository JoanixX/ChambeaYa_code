from app.adapters.output.orm.models.job_offer_model import JobOfferModel
from app.domain.entities.job_offer import JobOffer
from app.domain.repositories.job_offer_repository import JobOfferRepository
from sqlalchemy.future import select
from sqlalchemy import delete
from typing import Optional

class JobOfferRepositoryImpl(JobOfferRepository):
    def __init__(self, session):
        self.session = session

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
                embedding=model.embedding
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
                embedding=model.embedding
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
                    embedding=model.embedding
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