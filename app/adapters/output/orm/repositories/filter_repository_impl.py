from app.domain.repositories.filter_match_repository import FilterMatchRepository
from app.domain.entities.filter_match import FilterMatch
from app.adapters.output.orm.models.filter_match_model import FilterMatchModel

class FilterMatchRepositoryImpl(FilterMatchRepository):
    def __init__(self, session):
        self.session = session

    async def save(self, filter_match: FilterMatch):
        model = FilterMatchModel(
            job_offer_id=filter_match.job_offer_id,
            status=filter_match.status,
            stage=filter_match.stage
        )
        self.session.add(model)
        await self.session.commit()

    async def find_by_job_offer_id(self, job_offer_id: int, stage: int) -> FilterMatch:
        model = await self.session.get(FilterMatchModel, (job_offer_id, stage))
        if model:
            return FilterMatch(
                job_offer_id=model.job_offer_id,
                status=model.status,
                stage=model.stage
            )
        return None