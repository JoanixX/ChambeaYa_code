from pydantic import BaseModel, Field, EmailStr, validator
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session
from app.application.use_cases.register_company import RegisterCompanyUseCase
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse

class CompanyCreate(BaseModel):
    name: str = Field(..., description="Name of the company")
    tax_id: str = Field(..., description="Tax ID")
    industry: str = Field(..., description="Industry of the company")
    challenge_area_id: int = Field(..., description="Challenge area ID")
    challenge_description: str | None = Field(None, description="Challenge description")
    company_culture: str = Field(..., description="Company culture")
    required_hours: int = Field(..., description="Required hours")
    project_modality_id: int = Field(..., description="Project modality ID")
    contact_name: str = Field(..., description="Contact name for the company")
    email: EmailStr = Field(..., description="Email address of the company")

    @validator('name')
    def name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre de la compañía no puede estar vacío')
        return v

    @validator('tax_id')
    def tax_id_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('El tax_id no puede estar vacío')
        return v

    @validator('industry')
    def industry_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('La industria no puede estar vacía')
        return v

    @validator('company_culture')
    def company_culture_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('La cultura de la empresa no puede estar vacía')
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
        tax_id=company.tax_id,
        industry=company.industry,
        challenge_area_id=company.challenge_area_id,
        challenge_description=company.challenge_description,
        company_culture=company.company_culture,
        required_hours=company.required_hours,
        project_modality_id=company.project_modality_id,
        contact_name=company.contact_name,
        email=company.email,
        session=session
    )
    return {
        "id": new_company.id,
        "name": new_company.name,
        "tax_id": new_company.tax_id,
        "industry": new_company.industry,
        "challenge_area_id": new_company.challenge_area_id,
        "challenge_description": new_company.challenge_description,
        "company_culture": new_company.company_culture,
        "required_hours": new_company.required_hours,
        "project_modality_id": new_company.project_modality_id,
        "contact_name": new_company.contact_name,
        "email": new_company.email
    }