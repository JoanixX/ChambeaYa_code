from app.domain.entities.job_offer import JobOffer
from sqlalchemy.future import select

async def get_all_job_offers(session):
    result = await session.execute(select(JobOffer))
    return result.scalars().all()
