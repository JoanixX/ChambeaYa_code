from pydantic import BaseModel, Field, EmailStr, validator
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session
from app.application.use_cases.register_company import RegisterCompanyUseCase

class CompanyCreate(BaseModel):
    name: str = Field(..., description="Name of the company")
    industry: str = Field(..., description="Industry of the company")
    contact_name: str = Field(..., description="Contact name for the company")
    email: EmailStr = Field(..., description="Email address of the company")

    @validator('name')
    def name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre de la compañía no puede estar vacío')
        return v

    @validator('industry')
    def industry_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('La industria no puede estar vacía')
        return v

    @validator('contact_name')
    def contact_name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre de contacto no puede estar vacío')
        return v

router = APIRouter()

@router.post("/register/company")
async def register_company(company: CompanyCreate, session: AsyncSession = Depends(get_session)):
    use_case = RegisterCompanyUseCase()
    new_company = await use_case.register(
        name=company.name,
        industry=company.industry,
        contact_name=company.contact_name,
        email=company.email,
        session=session
    )
    return {
        "id": new_company.id,
        "name": new_company.name,
        "industry": new_company.industry,
        "contact_name": new_company.contact_name,
        "email": new_company.email
    }
