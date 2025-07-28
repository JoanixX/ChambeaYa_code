from pydantic import BaseModel, Field, EmailStr
from app.adapters.input.fastapi.validators import not_empty, not_in_future, in_range, positive_int, in_choices
from datetime import date
from typing import Optional,Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session
from app.application.use_cases.agreement_use_case import AgreementUseCase
from app.adapters.output.orm.repositories.agreement_repository_impl import AgreementRepositoryImpl
from app.domain.services.agreement_service import AgreementService
from app.application.ports.agreement_port import AgreementPort
from app.domain.entities.agreement import Agreement
from fastapi.responses import JSONResponse
import logging
from pydantic import field_validator

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgreementCreate(BaseModel):
    job_offer_id: int = Field(..., description="ID de la oferta de trabajo")
    student_id: int = Field(..., description="ID del estudiante")
    status: str = Field(..., description="Estado del acuerdo")
    start_date: Optional[date] = Field(None, description="Fecha de inicio")
    end_date: Optional[date] = Field(None, description="Fecha de fin")

    @field_validator('job_offer_id', 'student_id','status', 'start_date', 'end_date')
    def not_empty(cls, v, info):
        return not_empty(v, info.field_name)

    @field_validator('job_offer_id')
    def job_offer_id_positive(cls, v, info):
        return positive_int(v, 'El ID de la oferta de trabajo debe ser positivo')
    
    @field_validator('student_id')
    def student_id_positive(cls, v, info):
        return positive_int(v, 'El ID del estudiante debe ser positivo')

    @field_validator('start_date')
    def start_date_not_in_future(cls, v, info):
        return not_in_future(v, 'La fecha de inicio no puede ser en el futuro')

    @field_validator('end_date')
    def end_date_after_start(cls, v, info):
        start_date = info.data.get('start_date') if info.data else None
        if v and start_date:
            if v <= start_date:
                raise ValueError('La fecha de fin debe ser posterior a la fecha de inicio')
        return v

router = APIRouter()

class AgreementPortImpl(AgreementPort):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.agreement_repo = AgreementRepositoryImpl(session)

    async def register_agreement(self, agreement_data: Dict[str, Any]) -> Agreement:
        agreement = Agreement(
            id=0,
            job_offer_id=agreement_data['job_offer_id'],
            student_id=agreement_data['student_id'],
            status=agreement_data.get('status', 'pending'),
            start_date=agreement_data.get('start_date'),
            end_date=agreement_data.get('end_date')
        )

        saved_agreement = await self.agreement_repo.save(agreement)
        return saved_agreement

    async def get_agreement(self, agreement_id: int) -> Optional[Agreement]:
        return await self.agreement_repo.find_by_id(agreement_id)
    
    async def check_agreement_exists(self, job_offer_id: int, student_id: int) -> bool:
        agreement = await self.agreement_repo.find_active_agreement(job_offer_id, student_id)
        return agreement is not None
    
    async def get_all_agreements(self) -> list[Agreement]:
        return await self.agreement_repo.get_all()
    
    async def get_student_agreements(self, student_id: int) -> list[Agreement]:
        return await self.agreement_repo.find_by_student_id(student_id)
    
    async def get_job_offer_agreements(self, job_offer_id: int) -> list[Agreement]:
        return await self.agreement_repo.find_by_job_offer_id(job_offer_id)

    async def update_agreement(self, agreement_id: int, agreement_data: Dict[str, Any]) -> Optional[Agreement]:
        existing_agreement = await self.agreement_repo.find_by_id(agreement_id)
        if not existing_agreement:
            return None
        
        updated_agreement = Agreement(
            id=agreement_id,
            job_offer_id=agreement_data.get('job_offer_id', existing_agreement.job_offer_id),
            student_id=agreement_data.get('student_id', existing_agreement.student_id),
            status=agreement_data.get('status', existing_agreement.status),
            start_date=agreement_data.get('start_date', existing_agreement.start_date),
            end_date=agreement_data.get('end_date', existing_agreement.end_date)
        )

        return await self.agreement_repo.update(updated_agreement)
    
    async def delete_agreement(self, agreement_id: int) -> bool:
        return await self.agreement_repo.delete(agreement_id)
    
    async def validate_agreement_data(self, agreement_data: Dict[str, Any]) -> bool:
        logger.info("Validando datos del acuerdo: {agreement_data}")
        required_fields = ['job_offer_id', 'student_id', 'status', 'start_date', 'end_date']

        for field in required_fields:
            if field not in agreement_data or not agreement_data[field]:
                logger.error(f"Campo faltante o vacío: {field}")
                return False
            
        if agreement_data['start_date'] and agreement_data['end_date']:
            if agreement_data['end_date'] <= agreement_data['start_date']:
                logger.error("La fecha de fin debe ser posterior a la fecha de inicio.")
                return False
        
        logger.info("Validación exitosa")
        return True

@router.post("/register/agreement", response_model=dict, tags=["Agreement"])
async def register_agreement(request: Request, agreement: AgreementCreate, session: AsyncSession = Depends(get_session)):
    try:
        body = await request.body()
        logger.info(f"Datos recibidos para registrar acuerdo: {body.decode()}")

        agreement_port = AgreementPortImpl(session)
        agreement_repo = AgreementRepositoryImpl(session)
        greement_service = AgreementService(agreement_repo)
        
        use_case = AgreementUseCase(agreement_port, greement_service)
        logger.info(f"Iniciando registro del acuerdo: {agreement.job_offer_id} para el estudiante: {agreement.student_id}")
        result = await use_case.register_agreement(agreement.dict())

        logger.info(f"Acuerdo registrado exitosamente: {result}")
        return JSONResponse(content=result)
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error al registrar el acuerdo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/agreement/{agreement_id}", response_model=dict, tags=["Agreement"])
async def get_agreement(agreement_id: int, session: AsyncSession = Depends(get_session)):
    try:
        agreement_port = AgreementPortImpl(session)
        agreement_repo = AgreementRepositoryImpl(session)
        agreement_service = AgreementService(agreement_repo)
        agreement_use_case = AgreementUseCase(agreement_port, agreement_service)
        agreement = await agreement_use_case.get_agreement(agreement_id)

        return agreement.__dict__
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error al obtener el acuerdo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/student/{student_id}/agreements", response_model=dict, tags=["Agreement"])
async def get_student_agreements(student_id: int, session: AsyncSession = Depends(get_session)):
    try:
        agreement_port = AgreementPortImpl(session)
        agreement_repo = AgreementRepositoryImpl(session)
        agreement_service = AgreementService(agreement_repo)
        agreement_use_case = AgreementUseCase(agreement_port, agreement_service)
        agreement = await agreement_use_case.get_student_agreements(student_id)

        return [a.__dict__ for a in agreement]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error al obtener acuerdos del estudiante: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    
@router.get("/job_offer/{job_offer_id}/agreements", response_model=dict, tags=["Agreement"])
async def get_job_offer_agreements(job_offer_id: int, session: AsyncSession = Depends(get_session)):
    try:
        agreement_port = AgreementPortImpl(session)
        agreement_repo = AgreementRepositoryImpl(session)
        agreement_service = AgreementService(agreement_repo)
        agreement_use_case = AgreementUseCase(agreement_port, agreement_service)
        agreements = await agreement_use_case.get_job_offer_agreements(job_offer_id)

        return [a.__dict__ for a in agreements]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error al obtener acuerdos de la oferta de trabajo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/agreement/all", response_model=list, tags=["Agreement"])
async def get_all_agreements(session: AsyncSession = Depends(get_session)):
    try:
        agreement_port = AgreementPortImpl(session)
        agreement_repo = AgreementRepositoryImpl(session)
        agreement_service = AgreementService(agreement_repo)
        agreement_use_case = AgreementUseCase(agreement_port, agreement_service)
        agreements = await agreement_use_case.get_all_agreements()

        return [a.__dict__ for a in agreements]
    except Exception as e:
        logger.error(f"Error al obtener acuerdos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.put("/agreement/{agreement_id}", response_model=dict, tags=["Agreement"])
async def update_agreement(agreement_id: int, agreement: AgreementCreate, session: AsyncSession = Depends(get_session)):
    try:
        agreement_port = AgreementPortImpl(session)
        agreement_repo = AgreementRepositoryImpl(session)
        agreement_service = AgreementService(agreement_repo)
        agreement_use_case = AgreementUseCase(agreement_port, agreement_service)
        updated_agreement = await agreement_use_case.update_agreement(agreement_id, agreement.dict())
        
        return updated_agreement.__dict__
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error al actualizar acuerdo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.delete("/agreement/{agreement_id}", response_model=dict, tags=["Agreement"])
async def delete_agreement(agreement_id: int, session: AsyncSession = Depends(get_session)):
    try:
        agreement_port = AgreementPortImpl(session)
        agreement_repo = AgreementRepositoryImpl(session)
        agreement_service = AgreementService(agreement_repo)
        agreement_use_case = AgreementUseCase(agreement_port, agreement_service)
        deleted_agreement = await agreement_use_case.delete_agreement(agreement_id)

        return deleted_agreement
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error al eliminar acuerdo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")