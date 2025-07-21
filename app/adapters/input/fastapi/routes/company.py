from pydantic import BaseModel, Field, EmailStr, validator
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session
from app.application.use_cases.register_company import RegisterCompanyUseCase
from app.adapters.output.orm.repositories.company_repository_impl import CompanyRepositoryImpl
from app.domain.services.register_company_service import RegisterCompanyService
from app.application.ports.register_company_port import RegisterCompanyPort
from fastapi.responses import JSONResponse
from sqlalchemy.future import select
from app.domain.entities.company import Company
from app.adapters.output.orm.models.company_area_model import CompanyAreaModel

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

class CompanyPortImpl(RegisterCompanyPort):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.company_repo = CompanyRepositoryImpl(session)

    async def register_company(self, company):
        return await self.company_repo.save(company)

    async def validate_company_data(self, company_data: dict) -> bool:
        # Validaciones básicas
        required_fields = ['RUC', 'name', 'location', 'industry', 'area_id', 
                         'contact_name', 'email', 'company_culture']
        
        for field in required_fields:
            if field not in company_data or not company_data[field]:
                return False
        
        # Validaciones específicas
        if len(company_data['RUC']) != 11:  # RUC peruano
            return False
        
        return True

    async def check_ruc_exists(self, ruc: str) -> bool:
        company = await self.company_repo.find_by_ruc(ruc)
        return company is not None

    async def check_email_exists(self, email: str) -> bool:
        company = await self.company_repo.find_by_email(email)
        return company is not None

@router.post("/register/company")
async def register_company(company: CompanyCreate, session: AsyncSession = Depends(get_session)):
    try:
        # Crear adaptadores
        company_port = CompanyPortImpl(session)
        company_repo = CompanyRepositoryImpl(session)
        register_company_service = RegisterCompanyService(company_repo, company_port)
        
        # Crear caso de uso
        use_case = RegisterCompanyUseCase(company_port, register_company_service)
        
        # Ejecutar caso de uso
        result = await use_case.execute(company.dict())
        
        return JSONResponse(content=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")