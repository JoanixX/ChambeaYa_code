from app.application.ports.register_company_port import RegisterCompanyPort
from app.domain.entities.company import Company
from sqlalchemy.ext.asyncio import AsyncSession

class RegisterCompanyUseCase(RegisterCompanyPort):
    async def register(self, *, name: str, industry: str, contact_name: str, email: str, session: AsyncSession):
        new_company = Company(
            name=name,
            industry=industry,
            contact_name=contact_name,
            email=email
        )
        session.add(new_company)
        await session.commit()
        await session.refresh(new_company)
        return new_company
