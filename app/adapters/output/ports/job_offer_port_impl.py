from typing import Dict, Any, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from datetime import datetime

from app.adapters.output.orm.repositories.job_offer_repository_impl import JobOfferRepositoryImpl
from app.application.ports.job_offer_port import JobOfferPort
from app.domain.entities.job_offer import JobOffer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JobOfferPortImpl(JobOfferPort):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.job_offer_repo = JobOfferRepositoryImpl(session)

    async def register_job_offer(self, job_offer_data: Dict[str, Any]) -> JobOffer:
        if 'created_at' not in job_offer_data:
            job_offer_data['created_at'] = datetime.now()
        if 'updated_at' not in job_offer_data:
            job_offer_data['updated_at'] = datetime.now()
        job_offer = JobOffer(
            id = 0,
            company_id=job_offer_data['company_id'],
            title=job_offer_data['title'],
            description=job_offer_data['description'],
            required_hours=job_offer_data['required_hours'],
            approximated_salary=job_offer_data['approximated_salary'],
            duration=job_offer_data['duration'],
            start_date=job_offer_data['start_date'],
            modality=job_offer_data['modality'],
            embedding={},
            created_at=job_offer_data['created_at'],
            updated_at=job_offer_data['updated_at'],
            deleted_at=job_offer_data.get('deleted_at')
        )
        saved_job_offer = await self.job_offer_repo.save(job_offer)
        return saved_job_offer
    
    async def get_job_offer(self, job_offer_id: int) -> Optional[JobOffer]:
        return await self.job_offer_repo.find_by_id(job_offer_id)

    async def get_job_offers_by_company_id(self, company_id: int) -> Optional[JobOffer]:
        return await self.job_offer_repo.find_by_company_id(company_id)

    async def get_all_job_offers(self) -> List[JobOffer]:
        return await self.job_offer_repo.get_all()
    
    async def update_job_offer(self, job_offer_id: int, job_offer_data: Dict[str, Any]) -> Optional[JobOffer]:
        existing_job_offer = await self.job_offer_repo.find_by_id(job_offer_id)
        if not existing_job_offer:
            return None
        if 'created_at' not in job_offer_data:
            job_offer_data['created_at'] = existing_job_offer.created_at
        if 'updated_at' not in job_offer_data:
            job_offer_data['updated_at'] = datetime.now()
        updated_job_offer = JobOffer(
            id=job_offer_id,
            company_id=job_offer_data.get('company_id', existing_job_offer.company_id),
            title=job_offer_data.get('title', existing_job_offer.title),
            description=job_offer_data.get('description', existing_job_offer.description),
            required_hours=job_offer_data.get('required_hours', existing_job_offer.required_hours),
            approximated_salary=job_offer_data.get('approximated_salary', existing_job_offer.approximated_salary),
            duration=job_offer_data.get('duration', existing_job_offer.duration),
            start_date=job_offer_data.get('start_date', existing_job_offer.start_date),
            modality=job_offer_data.get('modality', existing_job_offer.modality),
            embedding=job_offer_data.get('embedding', existing_job_offer.embedding),
            created_at=job_offer_data['created_at'],
            updated_at=job_offer_data['updated_at'],
            deleted_at=job_offer_data.get('deleted_at', existing_job_offer.deleted_at)
        )
        return await self.job_offer_repo.update(updated_job_offer)
    
    async def delete_job_offer(self, job_offer_id: int) -> bool:
        return await self.job_offer_repo.delete(job_offer_id)
    
    async def validate_job_offer_data(self, job_offer_data: Dict[str, Any]) -> bool:
        logger.info(f"Validando datos de la oferta de trabajo: {job_offer_data}")

        required_fields = ['company_id', 'title', 'description', 'required_hours',
                           'approximated_salary', 'duration', 'start_date', 'modality']
        
        for field in required_fields:
            if field not in job_offer_data or not job_offer_data[field]:
                logger.error(f"Campo requerido faltante: {field}")
                return False
            
        logger.info("Validación exitosa")
        return True
    
    async def get_enriched_job_offers(self) -> List[JobOffer]:
        return await self.job_offer_repo.get_enriched_job_offers(self.session)