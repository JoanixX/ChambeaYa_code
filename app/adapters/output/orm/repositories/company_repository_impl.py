from app.domain.repositories.company_repository import CompanyRepository
from app.domain.entities.company import Company
from app.adapters.output.orm.models.company_model import CompanyModel
from sqlalchemy.future import select
from sqlalchemy import delete
from typing import Optional

class CompanyRepositoryImpl(CompanyRepository):
    def __init__(self, session):
        self.session = session

    async def save(self, company: Company):
        model = CompanyModel(
            RUC=company.RUC,
            name=company.name,
            location=company.location,
            industry=company.industry,
            area_id=company.area_id,
            contact_name=company.contact_name,
            email=company.email,
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
                RUC=model.RUC,
                name=model.name,
                location=model.location,
                industry=model.industry,
                area_id=model.area_id,
                contact_name=model.contact_name,
                email=model.email,
                company_culture=model.company_culture
            )
        return None

    async def find_by_ruc(self, ruc: str) -> Optional[Company]:
        result = await self.session.execute(select(CompanyModel).where(CompanyModel.RUC == ruc))
        model = result.scalar_one_or_none()
        if model:
            return Company(
                id=model.id,
                RUC=model.RUC,
                name=model.name,
                location=model.location,
                industry=model.industry,
                area_id=model.area_id,
                contact_name=model.contact_name,
                email=model.email,
                company_culture=model.company_culture
            )
        return None

    async def find_by_email(self, email: str) -> Optional[Company]:
        result = await self.session.execute(select(CompanyModel).where(CompanyModel.email == email))
        model = result.scalar_one_or_none()
        if model:
            return Company(
                id=model.id,
                RUC=model.RUC,
                name=model.name,
                location=model.location,
                industry=model.industry,
                area_id=model.area_id,
                contact_name=model.contact_name,
                email=model.email,
                company_culture=model.company_culture
            )
        return None

    async def get_all(self) -> list[Company]:
        result = await self.session.execute(select(CompanyModel))
        models = result.scalars().all()
        companies = []
        for model in models:
            companies.append(Company(
                id=model.id,
                RUC=model.RUC,
                name=model.name,
                location=model.location,
                industry=model.industry,
                area_id=model.area_id,
                contact_name=model.contact_name,
                email=model.email,
                company_culture=model.company_culture
            ))
        return companies

    async def update(self, company: Company) -> Optional[Company]:
        result = await self.session.execute(select(CompanyModel).where(CompanyModel.id == company.id))
        model = result.scalar_one_or_none()
        if model:
            model.RUC = company.RUC
            model.name = company.name
            model.location = company.location
            model.industry = company.industry
            model.area_id = company.area_id
            model.contact_name = company.contact_name
            model.email = company.email
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