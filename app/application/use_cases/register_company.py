from app.application.ports.register_company_port import RegisterCompanyPort
from app.domain.entities.company import Company
from sqlalchemy.ext.asyncio import AsyncSession

class RegisterCompanyUseCase(RegisterCompanyPort):
    async def register(
        self,
        *,
        name: str,
        tax_id: str,
        industry: str,
        challenge_area_id: int,
        challenge_description: str | None,
        company_culture: str,
        required_hours: int,
        project_modality_id: int,
        contact_name: str,
        email: str,
        session: AsyncSession
    ):
        new_company = Company(
            name=name,
            tax_id=tax_id,
            industry=industry,
            challenge_area_id=challenge_area_id,
            challenge_description=challenge_description,
            company_culture=company_culture,
            required_hours=required_hours,
            project_modality_id=project_modality_id,
            contact_name=contact_name,
            email=email
        )
        session.add(new_company)
        await session.commit()
        await session.refresh(new_company)
        return new_company
