from app.domain.entities.job_offer import JobOffer
from app.domain.repositories.filter_match_repository import FilterMatchRepository
from app.application.ports.run_filter_match_port import RunFilterMatchPort
from app.domain.entities.filter_match import FilterMatch

class FilterMatchService:
    def __init__(self, filter_match_repo: FilterMatchRepository, filter_match_port: RunFilterMatchPort):
        self.filter_match_repo = filter_match_repo
        self.filter_match_port = filter_match_port

    async def process_and_save(self, job_offer: JobOffer):
        #se llama a la ia a través del port 
        result = await self.filter_match_port.preprocess_job_offer(job_offer)
        
        #se crea la entidad de dominio para recibir los datos
        filter_match = FilterMatch(
            job_offer_id=result["job_offer_id"],
            status=result["status"],
            stage=result["stage"]
        )

        #se guarda en la base de datos el filter_match
        await self.filter_match_repo.save(filter_match)
        return filter_match