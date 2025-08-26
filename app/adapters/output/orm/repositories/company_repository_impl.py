from sqlalchemy.future import select
from sqlalchemy import delete
from typing import Optional

from app.domain.repositories.company_repository import CompanyRepository
from app.domain.entities.company import Company
from app.adapters.output.orm.models.company_model import CompanyModel

class CompanyRepositoryImpl(CompanyRepository):
    def __init__(self, session):
        self.session = session

    async def save(self, company: Company):
        model = CompanyModel(
            name=company.name,
            industry=company.industry,
            company_culture=company.company_culture
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def find_by_id(self, company_id: int) -> Optional[Company]:
        result = await self.session.execute(select(CompanyModel).where(CompanyModel.id == company_id))
        model = result.scalar_one_or_none()
        if model:
            return Company(
                id=model.id,
                name=model.name,
                industry=model.industry,
                company_culture=model.company_culture,
                created_at=model.created_at,
                updated_at=model.updated_at,
                deleted_at=model.deleted_at
            )
        return None

    async def get_all(self) -> list[Company]:
        result = await self.session.execute(select(CompanyModel))
        models = result.scalars().all()
        companies = []
        for model in models:
            companies.append(Company(
                id=model.id,
                name=model.name,
                industry=model.industry,
                company_culture=model.company_culture,
                created_at=model.created_at,
                updated_at=model.updated_at,
                deleted_at=model.deleted_at
            ))
        return companies

    async def update(self, company: Company) -> Optional[Company]:
        result = await self.session.execute(select(CompanyModel).where(CompanyModel.id == company.id))
        model = result.scalar_one_or_none()
        if model:
            model.name = company.name
            model.industry = company.industry
            model.company_culture = company.company_culture
            await self.session.commit()
            await self.session.refresh(model)
            return company
        return None

    async def delete(self, company_id: int):
        result = await self.session.execute(select(CompanyModel).where(CompanyModel.id == company_id))
        model = result.scalar_one_or_none()
        if not model:
            return False

        await self.session.execute(delete(CompanyModel).where(CompanyModel.id == company_id))
        await self.session.commit()
        return True