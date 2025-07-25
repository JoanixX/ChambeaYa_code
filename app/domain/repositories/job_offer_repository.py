from app.domain.entities.job_offer import JobOffer
from sqlalchemy.future import select

async def get_all_job_offers(session):
    result = await session.execute(select(JobOffer))
    return result.scalars().all()

async def get_job_offer_by_id(session, job_offer_id: int):
    result = await session.execute(select(JobOffer).where(JobOffer.id == job_offer_id))
    return result.scalar_one_or_none()
