from sqlalchemy.future import select
from app.adapters.output.orm.models.job_offer_model import JobOfferModel
from app.domain.entities.job_offer import JobOffer

# Mapper ORM -> Entidad de dominio

def job_offer_model_to_entity(model: JobOfferModel) -> JobOffer:
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
        requirements=model.requirements,
        embedding=model.embedding
    )

async def get_all_job_offers_impl(session):
    result = await session.execute(select(JobOfferModel))
    models = result.scalars().all()
    return [job_offer_model_to_entity(m) for m in models]

async def get_job_offer_by_id_impl(session, job_offer_id: int):
    result = await session.execute(select(JobOfferModel).where(JobOfferModel.id == job_offer_id))
    model = result.scalar_one_or_none()
    return job_offer_model_to_entity(model) if model else None
