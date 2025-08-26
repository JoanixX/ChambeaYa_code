from app.domain.entities.company_area import CompanyArea
from app.domain.repositories.company_area_repository import CompanyAreaRepository
from typing import List

class CompanyAreaService:
    def __init__(self, company_area_repo: CompanyAreaRepository):
        self.company_area_repo = company_area_repo

    async def add_company_area(self, company_area: CompanyArea) -> CompanyArea:
        exists = await self.company_area_repo.exists(company_area.company_id, company_area.area_id)

        if exists:
            raise ValueError("La compañia ya tiene esta área asignada")

        saved_model = await self.company_area_repo.save(company_area)

        if saved_model:
            return saved_model
        else:
            raise ValueError("Error al guardar el área de la compañia")

    async def get_company_areas(self, company_id: int) -> List[CompanyArea]:
        return await self.company_area_repo.get_by_company_id(company_id)

    async def delete_company_area(self, company_id: int, area_id: int) -> bool:
        return await self.company_area_repo.delete(company_id, area_id)