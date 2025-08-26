from typing import List
from sqlalchemy.future import select
from sqlalchemy import delete
from app.domain.entities.job_offer_area import JobOfferArea
from app.domain.repositories.job_offer_area_repository import JobOfferAreaRepository
from app.adapters.output.orm.models.job_offer_area_model import JobOfferAreaModel

class JobOfferAreaRepositoryImpl(JobOfferAreaRepository):
    def __init__(self, session):
        self.session = session

    async def get_by_job_offer_id(self, job_offer_id: int) -> List[JobOfferArea]:
        result = await self.session.execute(
            select(JobOfferAreaModel).where(JobOfferAreaModel.job_offer_id == job_offer_id)
        )
        models = result.scalars().all()
        areas = []
        for model in models:
            areas.append(
                JobOfferArea(
                    job_offer_id=model.job_offer_id, 
                    area_id=model.area_id
                )
            )
        return areas

    async def exists(self, job_offer_id: int, area_id: int) -> bool:
        result = await self.session.execute(
            select(JobOfferAreaModel).where(
                JobOfferAreaModel.job_offer_id == job_offer_id,
                JobOfferAreaModel.area_id == area_id
            )
        )
        return result.scalar_one_or_none() is not None

    async def save(self, job_offer_area: JobOfferArea) -> JobOfferArea:
        exists = await self.exists(job_offer_area.job_offer_id, job_offer_area.area_id)
        if exists:
            return job_offer_area
        
        model = JobOfferAreaModel(
            job_offer_id=job_offer_area.job_offer_id,
            area_id=job_offer_area.area_id
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return JobOfferArea(job_offer_id=model.job_offer_id, area_id=model.area_id)

    async def delete(self, job_offer_id: int, area_id: int) -> bool:
        result = await self.session.execute(
            select(JobOfferAreaModel).where(
                JobOfferAreaModel.job_offer_id == job_offer_id,
                JobOfferAreaModel.area_id == area_id
            )
        )
        model = result.scalar_one_or_none()
        if not model:
            return False

        await self.session.execute(
            delete(JobOfferAreaModel).where(
                JobOfferAreaModel.job_offer_id == job_offer_id,
                JobOfferAreaModel.area_id == area_id
            )
        )
        await self.session.commit()
        return True