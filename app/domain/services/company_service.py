from typing import Dict, Any, Optional
from datetime import datetime

from app.domain.entities.company import Company
from app.domain.repositories.company_repository import CompanyRepository

class CompanyService:
    def __init__(self, company_repo: CompanyRepository):
        self.company_repo = company_repo

    async def register_company(self, company_data: Dict[str, Any]) -> int:
        company = self.company_entity(company_data)

        saved_model = await self.company_repo.save(company)
        if saved_model:
            return saved_model.id
        else:
            raise ValueError("Error al guardar la empresa")
    
    async def get_company(self, company_id: int) -> Optional[Company]:
        return await self.company_repo.find_by_id(company_id)

    async def get_all_companies(self) -> list[Company]:
        return await self.company_repo.get_all()
    
    async def update_company(self, company_id: int, company_data: Dict[str, Any]) -> Optional[Company]:
        existing_company = await self.company_repo.find_by_id(company_id)
        if not existing_company:
            return None

        updated_company = Company(
            id=company_id,
            name=company_data.get("name", existing_company.name),
            industry=company_data.get("industry", existing_company.industry),
            company_culture=company_data.get("company_culture", existing_company.company_culture)
        )

        await self.company_repo.update(updated_company)
        return updated_company
    
    async def delete_company(self, company_id: int) -> bool:
        return await self.company_repo.delete(company_id)
    
    def company_entity(self, company_data: Dict[str, Any]) -> Company:
        if 'created_at' not in company_data:
            company_data['created_at'] = datetime.now()
        if 'updated_at' not in company_data:
            company_data['updated_at'] = datetime.now()
        return Company(
            id=0,  #se asignará automáticamente por la base de datos
            name=company_data.get("name", None),
            industry=company_data.get("industry", None),
            company_culture=company_data.get("company_culture", None),
            created_at=company_data['created_at'],
            updated_at=company_data['updated_at']
        )