from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
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

async def create_job_offer_impl(session, job_offer: JobOffer):
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
        requirements=job_offer.requirements,
        embedding=job_offer.embedding
    )
    session.add(model)
    await session.commit()
    await session.refresh(model)
    return job_offer_model_to_entity(model)

async def update_job_offer_impl(session, job_offer: JobOffer):
    await session.execute(
        sqlalchemy_update(JobOfferModel)
        .where(JobOfferModel.id == job_offer.id)
        .values(
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
            requirements=job_offer.requirements,
            embedding=job_offer.embedding
        )
    )
    await session.commit()
    return await get_job_offer_by_id_impl(session, job_offer.id)

async def delete_job_offer_impl(session, job_offer_id: int):
    await session.execute(
        sqlalchemy_delete(JobOfferModel).where(JobOfferModel.id == job_offer_id)
    )
    await session.commit()
    return True
