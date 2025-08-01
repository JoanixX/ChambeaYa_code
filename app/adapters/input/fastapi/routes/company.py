from sqlalchemy.future import select
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Dict, Any, List, Optional
from datetime import date
import logging
from fastapi import APIRouter, Depends, HTTPException, Request, Body
from fastapi.responses import JSONResponse
from app.adapters.input.fastapi.validators import not_empty, not_in_future ,start_date_future, positive_int, in_choices
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session

from app.application.use_cases.company_use_case import CompanyUseCase
from app.adapters.output.orm.repositories.company_repository_impl import CompanyRepositoryImpl
from app.domain.services.company_service import CompanyService
from app.application.ports.company_port import CompanyPort
from app.domain.entities.company import Company
from app.adapters.output.orm.models.area_model import AreaModel

router = APIRouter()
# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CompanyCreate(BaseModel):
    RUC: str = Field(..., description="RUC de la empresa")
    name: str = Field(..., description="Nombre de la empresa")
    location: str = Field(..., description="Ubicación de la empresa")
    industry: str = Field(..., description="Industria de la empresa")
    area_id: int = Field(..., description="ID del área")
    contact_name: str = Field(..., description="Nombre del contacto")
    email: str = Field(..., description="Correo electrónico de la empresa")
    company_culture: str = Field(..., description="Cultura de la empresa")

    from pydantic import field_validator

    @field_validator('name', 'RUC', 'industry', 'company_culture', 'contact_name', 'location')
    def not_empty_fields(cls, v, info):
        return not_empty(v, info.field_name)
    
    @field_validator('email')
    def valid_email(cls, v):
        return EmailStr._validate(v)
    
    @field_validator('area_id')
    def experience_id_valid(cls, v, info):
        return positive_int(v, 'El ID del area')

class CompanyPortImpl(CompanyPort):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.company_repo = CompanyRepositoryImpl(session)

    async def register_company(self, company_data: Dict[str, Any]) -> Company:
        company = Company(
            id=0,
            RUC=company_data['RUC'],
            name=company_data['name'],
            location=company_data['location'],
            industry=company_data['industry'],
            area_id=company_data['area_id'],
            contact_name=company_data['contact_name'],
            email=company_data['email'],
            company_culture=company_data['company_culture']
        )

        saved_company = await self.company_repo.save(company)
        return saved_company
    
    async def get_all_companies(self) -> list[Company]:
        return await self.company_repo.get_all()

    async def get_company (self, company_id: int) -> Optional[Company]:
        return await self.company_repo.find_by_id(company_id)
    
    async def update_company(self, company_id: int, company_data: Dict[str, Any]) -> Optional[Company]:
        existing_company = await self.company_repo.find_by_id(company_id)
        if not existing_company:
            return None
        
        updated_company = Company(
            id=company_id,
            RUC=company_data.get('RUC', existing_company.RUC),
            name=company_data.get('name', existing_company.name),
            location=company_data.get('location', existing_company.location),
            industry=company_data.get('industry', existing_company.industry),
            area_id=company_data.get('area_id', existing_company.area_id),
            contact_name=company_data.get('contact_name', existing_company.contact_name),
            email=company_data.get('email', existing_company.email),
            company_culture=company_data.get('company_culture', existing_company.company_culture)
        )

        return await self.company_repo.update(updated_company)
    
    async def delete_company(self, company_id: int) -> bool:
        return await self.company_repo.delete(company_id)
    
    async def validate_company_data(self, company_data: Dict[str, Any]) -> bool:
        logger.info("Validando datos de la empresa: {company_data}")

        required_fields = ['RUC', 'name', 'location', 'industry', 'area_id',
                          'contact_name', 'email', 'company_culture']
        for field in required_fields:
            if field not in company_data or not company_data[field]:
                logger.error(f"Campo requerido '{field}' está vacío o no existe.")
                return False

        if company_data['RUC'] and len(company_data['RUC']) != 11:
            logger.error("El RUC debe tener 11 caracteres.")
            return False
        
        logger.info("Datos de la empresa validados correctamente.")
        return True
    
    async def check_email_exists(self, email: str) -> bool:
        company = await self.company_repo.find_by_email(email)
        return company is not None
    
    async def check_ruc_exists(self, ruc: str) -> bool:
        company = await self.company_repo.find_by_ruc(ruc)
        return company is not None

@router.post("/register/company", response_model=dict, tags=["Company"])
async def register_company(request: Request, company: CompanyCreate, session: AsyncSession = Depends(get_session)):
    try:
        body = await request.body()
        logger.info(f"Datos recibidos para registrar empresa: {body.decode()}")
        logger.info(f"Iniciando registro de la empresa: {company.email}")

        company_port = CompanyPortImpl(session)
        company_repo = CompanyRepositoryImpl(session)
        company_service = CompanyService(company_repo)
        
        use_case = CompanyUseCase(company_port, company_service)
        
        logger.info("Ejecutando caso de uso...")
        result = await use_case.register_company(company.dict())

        logger.info(f"Empresa registrada exitosamente: {result}")
        return JSONResponse(content=result)
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error al registrar la empresa: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/company/all", response_model=List[dict], tags=["Company"])
async def get_all_companies(session: AsyncSession = Depends(get_session)):
    try:
        company_port = CompanyPortImpl(session)
        company_repo = CompanyRepositoryImpl(session)
        company_service = CompanyService(company_repo)
        company_use_case = CompanyUseCase(company_port, company_service)
        company = await company_use_case.get_all_companies()

        return [comp.__dict__ for comp in company]
    except Exception as e:
        logger.error(f"Error al obtener empresas: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/company/{company_id}", response_model=dict, tags=["Company"])
async def get_company_by_id(company_id: int, session: AsyncSession = Depends(get_session)):
    try:
        company_port = CompanyPortImpl(session)
        company_repo = CompanyRepositoryImpl(session)
        company_service = CompanyService(company_repo)
        company_use_case = CompanyUseCase(company_port, company_service)
        company = await company_use_case.get_company(company_id)

        return company.__dict__
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error al obtener la empresa: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.put("/company/{company_id}", response_model=dict, tags=["Company"])
async def update_company(company_id: int, company: CompanyCreate, session: AsyncSession = Depends(get_session)):
    try:
        company_port = CompanyPortImpl(session)
        company_repo = CompanyRepositoryImpl(session)
        company_service = CompanyService(company_repo)
        company_use_case = CompanyUseCase(company_port, company_service)
        updated_company = await company_use_case.update_company(company_id, company.dict())

        return updated_company.__dict__
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error al actualizar la empresa: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.delete("/company/{company_id}", response_model=dict, tags=["Company"])
async def delete_company(company_id: int, session: AsyncSession = Depends(get_session)):
    try:
        company_port = CompanyPortImpl(session)
        company_repo = CompanyRepositoryImpl(session)
        company_service = CompanyService(company_repo)
        company_use_case = CompanyUseCase(company_port, company_service)
        deleted_company = await company_use_case.delete_company(company_id)

        return deleted_company
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error al eliminar la empresa: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")