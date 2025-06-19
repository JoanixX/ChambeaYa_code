from pydantic import BaseModel, Field, EmailStr, validator
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session
from app.application.use_cases.register_company import RegisterCompanyUseCase
from fastapi.responses import JSONResponse
from .jwt_utils import create_access_token, verify_password
from sqlalchemy.future import select
from app.domain.entities.company import Company

class CompanyCreate(BaseModel):
    RUC: str = Field(..., description="RUC de la empresa")
    name: str = Field(..., description="Nombre de la empresa")
    location: str = Field(..., description="Ubicación de la empresa")
    industry: str = Field(..., description="Industria de la empresa")
    area_id: int = Field(..., description="ID del área")
    contact_name: str = Field(..., description="Nombre del contacto")
    email: EmailStr = Field(..., description="Correo electrónico de la empresa")
    company_culture: str = Field(..., description="Cultura de la empresa")

    @validator('name')
    def name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre de la compañía no puede estar vacío')
        return v

    @validator('RUC')
    def ruc_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('El RUC no puede estar vacío')
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
        RUC=company.RUC,
        name=company.name,
        location=company.location,
        industry=company.industry,
        area_id=company.area_id,
        contact_name=company.contact_name,
        email=company.email,
        company_culture=company.company_culture,
        session=session
    )
    return JSONResponse(content={"id": new_company.id, "email": new_company.email, "name": new_company.name})