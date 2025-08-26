from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.company_area import CompanyArea
from app.adapters.output.orm.repositories.company_area_repository_impl import CompanyAreaRepositoryImpl
from app.application.ports.company_area_port import CompanyAreaPort

class CompanyAreaPortImpl(CompanyAreaPort):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.company_area_repo = CompanyAreaRepositoryImpl(session)

    async def add_company_area(self, company_area: CompanyArea) -> CompanyArea:
        return await self.company_area_repo.save(company_area)

    async def get_company_areas(self, company_id: int) -> List[CompanyArea]:
        return await self.company_area_repo.get_by_company_id(company_id)
    
    async def delete_company_area(self, company_id: int, area_id: int) -> bool:
        return await self.company_area_repo.delete(company_id, area_id)
    
    async def company_area_exists(self, company_id: int, area_id: int) -> bool:
        return await self.company_area_repo.exists(company_id, area_id)