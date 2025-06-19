from app.application.ports.register_company_port import RegisterCompanyPort
from app.domain.entities.company import Company
from sqlalchemy.ext.asyncio import AsyncSession

class RegisterCompanyUseCase(RegisterCompanyPort):
    async def register(
        self,
        *,
        RUC: str,
        name: str,
        location: str,
        industry: str,
        area_id: int,
        contact_name: str,
        email: str,
        company_culture: str,
        session: AsyncSession
    ):
        new_company = Company(
            RUC=RUC,
            name=name,
            location=location,
            industry=industry,
            area_id=area_id,
            contact_name=contact_name,
            email=email,
            company_culture=company_culture
        )
        session.add(new_company)
        await session.commit()
        await session.refresh(new_company)
        return new_company
