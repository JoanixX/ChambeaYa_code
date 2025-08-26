from typing import List
from sqlalchemy.future import select
from sqlalchemy import delete
from app.domain.entities.company_area import CompanyArea
from app.domain.repositories.company_area_repository import CompanyAreaRepository
from app.adapters.output.orm.models.company_area_model import CompanyAreaModel

class CompanyAreaRepositoryImpl(CompanyAreaRepository):
    def __init__(self, session):
        self.session = session

    async def get_by_company_id(self, company_id: int) -> List[CompanyArea]:
        result = await self.session.execute(
            select(CompanyAreaModel).where(CompanyAreaModel.company_id == company_id)
        )
        models = result.scalars().all()
        areas = []
        for model in models:
            areas.append(
                CompanyArea(
                    company_id=model.company_id, 
                    area_id=model.area_id
                )
            )
        return areas

    async def exists(self, company_id: int, area_id: int) -> bool:
        result = await self.session.execute(
            select(CompanyAreaModel).where(
                CompanyAreaModel.company_id == company_id,
                CompanyAreaModel.area_id == area_id
            )
        )
        return result.scalar_one_or_none() is not None

    async def save(self, company_area: CompanyArea) -> CompanyArea:
        exists = await self.exists(company_area.company_id, company_area.area_id)
        if exists:
            return company_area
        
        model = CompanyAreaModel(
            company_id=company_area.company_id,
            area_id=company_area.area_id
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return CompanyArea(company_id=model.company_id, area_id=model.area_id)

    async def delete(self, company_id: int, area_id: int) -> bool:
        result = await self.session.execute(
            select(CompanyAreaModel).where(
                CompanyAreaModel.company_id == company_id,
                CompanyAreaModel.area_id == area_id
            )
        )
        model = result.scalar_one_or_none()
        if not model:
            return False

        await self.session.execute(
            delete(CompanyAreaModel).where(
                CompanyAreaModel.company_id == company_id,
                CompanyAreaModel.area_id == area_id
            )
        )
        await self.session.commit()
        return True