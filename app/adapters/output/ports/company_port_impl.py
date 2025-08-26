from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from datetime import datetime

from app.adapters.output.orm.repositories.company_repository_impl import CompanyRepositoryImpl
from app.application.ports.company_port import CompanyPort
from app.domain.entities.company import Company

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CompanyPortImpl(CompanyPort):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.company_repo = CompanyRepositoryImpl(session)

    async def register_company(self, company_data: Dict[str, Any]) -> Company:
        if 'created_at' not in company_data:
            company_data['created_at'] = datetime.now()
        if 'updated_at' not in company_data:
            company_data['updated_at'] = datetime.now()
        company = Company(
            id=0,
            name=company_data['name'],
            industry=company_data['industry'],
            company_culture=company_data['company_culture'],
            created_at=company_data['created_at'],
            updated_at=company_data['updated_at'],
            deleted_at=company_data.get('deleted_at')
        )

        saved_company = await self.company_repo.save(company)
        return saved_company
    
    async def get_all_companies(self) -> list[Company]:
        return await self.company_repo.get_all()

    async def get_company (self, company_id: int) -> Optional[Company]:
        return await self.company_repo.find_by_id(company_id)
    
    async def update_company(self, company_id: int, company_data: Dict[str, Any]) -> Optional[Company]:
        existing_company = await self.company_repo.find_by_id(company_id)
        if not existing_company:
            return None
        if 'created_at' not in company_data:
            company_data['created_at'] = existing_company.created_at
        if 'updated_at' not in company_data:
            company_data['updated_at'] = datetime.now()
        
        updated_company = Company(
            id=company_id,
            name=company_data.get('name', existing_company.name),
            industry=company_data.get('industry', existing_company.industry),
            company_culture=company_data.get('company_culture', existing_company.company_culture),
            created_at=company_data['created_at'],
            updated_at=company_data['updated_at'],
            deleted_at=company_data.get('deleted_at', existing_company.deleted_at)
        )

        return await self.company_repo.update(updated_company)
    
    async def delete_company(self, company_id: int) -> bool:
        return await self.company_repo.delete(company_id)
    
    async def validate_company_data(self, company_data: Dict[str, Any]) -> bool:
        logger.info("Validando datos de la empresa: {company_data}")

        required_fields = ['name', 'industry', 'company_culture']
        for field in required_fields:
            if field not in company_data or not company_data[field]:
                logger.error(f"Campo requerido '{field}' está vacío o no existe.")
                return False

        logger.info("Datos de la empresa validados correctamente.")
        return True