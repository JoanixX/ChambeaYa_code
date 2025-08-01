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

from app.domain.services.preprocess_job_offer_service import PreprocessJobOfferService
from app.application.use_cases.job_offer_use_case import JobOfferUseCase
from app.adapters.output.orm.repositories.job_offer_repository_impl import JobOfferRepositoryImpl
from app.adapters.output.orm.repositories.company_repository_impl import CompanyRepositoryImpl
from app.domain.services.job_offer_service import JobOfferService
from app.application.ports.job_offer_port import JobOfferPort
from app.domain.entities.job_offer import JobOffer
from app.adapters.output.orm.models.job_offer_required_skill_model import JobOfferRequiredSkillModel
from app.domain.entities.skill import Skill
from app.adapters.output.orm.repositories.skill_repository_impl import get_skill_by_id_impl

router = APIRouter()
# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_skills_for_job_offer(session: AsyncSession, job_offer_id: int) -> List[Skill]:
    skill_links_result = await session.execute(select(JobOfferRequiredSkillModel).
    where(JobOfferRequiredSkillModel.job_offer_id == job_offer_id))
    skill_links = skill_links_result.scalars().all()
    
    skills = []
    for link in skill_links:
        skill = await get_skill_by_id_impl(session, link.skill_id)
        if skill:
            skills.append(skill)
    return skills

class JobOfferCreate(BaseModel):
    company_id: int = Field(..., description="ID of the company")
    title: str = Field(..., description="Title of the job offer")
    description: str = Field(..., description="Description")
    required_hours: int = Field(..., description="Required hours")
    approximated_salary: int = Field(..., description="Approximated salary")
    duration: int = Field(..., description="Duration")
    start_date: date = Field(..., description="Start date")
    area_id: int = Field(..., description="Area ID")
    experience_id: int = Field(..., description="Experience ID")
    modality: int = Field(..., description="Modality")
    embedding: Optional[dict] = Field(None, description="Embedding")

    @field_validator("start_date")
    def start_date_validator(cls, v, info):
        return start_date_future(v, 'La fecha de inicio no puede ser en el pasado')
    
    @field_validator("required_hours", "approximated_salary", "duration")
    def not_empty_fields(cls, v, info):
            return not_empty(v, info.field_name)
    
    @field_validator('modality')
    def preferred_modality_valid(cls, v, info):
        return in_choices(v, [1, 2, 3], 'La modalidad preferida')
    
    @field_validator('experience_id')
    def experience_id_valid(cls, v, info):
        return positive_int(v, 'El ID de experiencia')
    
    @field_validator('area_id')
    def area_id_valid(cls, v, info):
        return positive_int(v, 'El ID del area')

class JobOfferPortImpl(JobOfferPort):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.job_offer_repo = JobOfferRepositoryImpl(session)

    async def register_job_offer(self, job_offer_data: Dict[str, Any]) -> JobOffer:
        job_offer = JobOffer(
            id = 0,
            company_id=job_offer_data['company_id'],
            title=job_offer_data['title'],
            description=job_offer_data['description'],
            required_hours=job_offer_data['required_hours'],
            approximated_salary=job_offer_data['approximated_salary'],
            duration=job_offer_data['duration'],
            start_date=job_offer_data['start_date'],
            area_id=job_offer_data("area_id", None),
            experience_id=job_offer_data("experience_id", None),
            modality=job_offer_data['modality'],
            embedding={}
        )
    
        saved_job_offer = await self.job_offer_repo.save(job_offer)
        return saved_job_offer
    
    async def get_job_offer(self, job_offer_id: int) -> Optional[JobOffer]:
        return await self.job_offer_repo.find_by_id(job_offer_id)

    async def get_job_offer_by_company_id(self, company_id: int) -> Optional[JobOffer]:
        return await self.job_offer_repo.find_by_company_id(company_id)

    async def get_all_job_offers(self) -> List[JobOffer]:
        return await self.job_offer_repo.get_all()
    
    async def update_job_offer(self, job_offer_id: int, job_offer_data: Dict[str, Any]) -> Optional[JobOffer]:
        existing_job_offer = await self.job_offer_repo.find_by_id(job_offer_id)
        if not existing_job_offer:
            return None
        
        updated_job_offer = JobOffer(
            id=job_offer_id,
            company_id=job_offer_data.get('company_id', existing_job_offer.company_id),
            title=job_offer_data.get('title', existing_job_offer.title),
            description=job_offer_data.get('description', existing_job_offer.description),
            required_hours=job_offer_data.get('required_hours', existing_job_offer.required_hours),
            approximated_salary=job_offer_data.get('approximated_salary', existing_job_offer.approximated_salary),
            duration=job_offer_data.get('duration', existing_job_offer.duration),
            start_date=job_offer_data.get('start_date', existing_job_offer.start_date),
            area_id=job_offer_data.get('area_id', None),
            experience_id=job_offer_data.get('experience_id', None),
            modality=job_offer_data.get('modality', existing_job_offer.modality),
            embedding=job_offer_data.get('embedding', existing_job_offer.embedding)
        )
        return await self.job_offer_repo.update(updated_job_offer)
    
    async def delete_job_offer(self, job_offer_id: int) -> bool:
        return await self.job_offer_repo.delete(job_offer_id)
    
    async def validate_job_offer_data(self, job_offer_data: Dict[str, Any]) -> bool:
        logger.info(f"Validando datos de la oferta de trabajo: {job_offer_data}")

        required_fields = ['company_id', 'title', 'description', 'required_hours',
                           'approximated_salary', 'duration', 'start_date', 'area_id',
                           'experience_id', 'modality']
        
        for field in required_fields:
            if field not in job_offer_data or not job_offer_data[field]:
                logger.error(f"Campo requerido faltante: {field}")
                return False
            
        logger.info("Validación exitosa")
        return True

@router.post("/register/job_offer", response_model=dict, tags=["Job Offer"])
async def register_job_offer(request: Request, job_offer: JobOfferCreate, session: AsyncSession = Depends(get_session)):
    try:
        body = await request.body()
        logger.info(f"Body recibido: {body.decode()}")
        logger.info(f"Iniciando registro de oferta de trabajo: {job_offer.title}")

        job_offer_port = JobOfferPortImpl(session)
        job_offer_repo = JobOfferRepositoryImpl(session)
        job_offer_service = JobOfferService(job_offer_repo)
        use_case = JobOfferUseCase(job_offer_port, job_offer_service)

        logger.info("Ejecutando caso de uso...")
        result = await use_case.register_job_offer(job_offer.dict())
        logger.info(f"Oferta de trabajo registrada con éxito: {result}")
        return JSONResponse(content=result)
    
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error al registrar oferta de trabajo: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/job_offer/all", response_model=List[dict], tags=["Job Offer"])
async def get_all_job_offers(session: AsyncSession = Depends(get_session)):
    try:
        job_offer_port = JobOfferPortImpl(session)
        job_offer_repo = JobOfferRepositoryImpl(session)
        job_offer_service = JobOfferService(job_offer_repo)
        use_case = JobOfferUseCase(job_offer_port, job_offer_service)
        job_offers = await use_case.get_all_job_offers()

        def serialize_job_offer(j):
            d = j.__dict__.copy()
            if d.get('start_date'):
                d['start_date'] = d['start_date'].isoformat()
            return d
        
        return [serialize_job_offer(j) for j in job_offers]
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/job_offer/{job_offer_id}", response_model=dict, tags=["Job Offer"])
async def get_job_offer(job_offer_id: int, session: AsyncSession = Depends(get_session)):
    try:
        job_offer_port = JobOfferPortImpl(session)
        job_offer_repo = JobOfferRepositoryImpl(session)
        job_offer_service = JobOfferService(job_offer_repo)
        use_case = JobOfferUseCase(job_offer_port, job_offer_service)
        job_offer = await use_case.get_job_offer(job_offer_id)
        return job_offer.__dict__
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/job_offer/company/{company_id}", response_model=dict, tags=["Job Offer"])
async def get_job_offer_by_company_id(company_id: int, session: AsyncSession = Depends(get_session)):
    try:
        job_offer_port = JobOfferPortImpl(session)
        job_offer_repo = JobOfferRepositoryImpl(session)
        job_offer_service = JobOfferService(job_offer_repo)
        use_case = JobOfferUseCase(job_offer_port, job_offer_service)
        job_offer = await use_case.get_job_offer_by_company_id(company_id)
        if not job_offer:
            raise HTTPException(status_code=404, detail="Job offer not found")
        return job_offer.__dict__
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.put("/job_offer/{job_offer_id}", response_model=dict, tags=["Job Offer"])
async def update_job_offer_endpoint(job_offer_id: int, job_offer: JobOfferCreate, session: AsyncSession = Depends(get_session)):
    try:
        job_offer_port = JobOfferPortImpl(session)
        job_offer_repo = JobOfferRepositoryImpl(session)
        job_offer_service = JobOfferService(job_offer_repo)
        use_case = JobOfferUseCase(job_offer_port, job_offer_service)
        updated = await use_case.update_job_offer(job_offer_id, job_offer.dict())
        
        return updated.__dict__
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.delete("/job_offer/{job_offer_id}", response_model=dict, tags=["Job Offer"])
async def delete_job_offer_endpoint(job_offer_id: int, session: AsyncSession = Depends(get_session)):
    try:
        job_offer_port = JobOfferPortImpl(session)
        job_offer_repo = JobOfferRepositoryImpl(session)
        job_offer_service = JobOfferService(job_offer_repo)
        use_case = JobOfferUseCase(job_offer_port, job_offer_service)
        deleted = await use_case.delete_job_offer(job_offer_id)
        
        return deleted
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/job_offer/skills/{job_offer_id}", response_model=List[dict], tags=["Job Offer"])
async def get_skills_for_job_offer_endpoint(job_offer_id: int, session: AsyncSession = Depends(get_session)):
    skills = await get_skills_for_job_offer(session, job_offer_id)
    if not skills:
        return []
    return [{"id": skill.id, "name": skill.name} for skill in skills]