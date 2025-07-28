from pydantic import BaseModel, Field, validator
from app.adapters.input.fastapi.validators import not_in_future
from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session
from app.application.use_cases.agreement_use_case import AgreementUseCase
from app.adapters.output.orm.repositories.agreement_repository_impl import AgreementRepositoryImpl
from app.domain.services.agreement_service import AgreementService
from app.application.ports.agreement_port import AgreementPort
from fastapi.responses import JSONResponse

class AgreementCreate(BaseModel):
    job_offer_id: int = Field(..., description="ID de la oferta de trabajo")
    student_id: int = Field(..., description="ID del estudiante")
    start_date: Optional[date] = Field(None, description="Fecha de inicio")
    end_date: Optional[date] = Field(None, description="Fecha de fin")

    from pydantic import field_validator

    @field_validator('job_offer_id')
    def job_offer_id_positive(cls, v, info):
        if v <= 0:
            raise ValueError('El ID de la oferta de trabajo debe ser positivo')
        return v

    @field_validator('student_id')
    def student_id_positive(cls, v, info):
        if v <= 0:
            raise ValueError('El ID del estudiante debe ser positivo')
        return v

    @field_validator('end_date')
    def end_date_after_start(cls, v, info):
        # info.data contiene todos los valores del modelo
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

    async def register_agreement(self, agreement):
        return await self.agreement_repo.save(agreement)

    async def validate_agreement_data(self, agreement_data: dict) -> bool:
        # Validaciones básicas
        required_fields = ['job_offer_id', 'student_id']
        
        for field in required_fields:
            if field not in agreement_data:
                return False
        
        # Validaciones específicas
        if agreement_data['job_offer_id'] <= 0 or agreement_data['student_id'] <= 0:
            return False
        
        return True

    async def check_agreement_exists(self, student_id: int, job_offer_id: int) -> bool:
        agreements = await self.agreement_repo.find_by_student_id(student_id)
        return any(agreement.job_offer_id == job_offer_id for agreement in agreements)

    async def update_agreement_status(self, agreement_id: int, status: str):
        agreement = await self.agreement_repo.find_by_id(agreement_id)
        if agreement:
            # Actualizar status
            await self.agreement_repo.update(agreement)
            return agreement
        return None

@router.post("/register/agreement", response_model=dict, tags=["Agreement"])
async def register_agreement(agreement: AgreementCreate, session: AsyncSession = Depends(get_session)):
    try:
        # Crear adaptadores
        agreement_port = AgreementPortImpl(session)
        agreement_repo = AgreementRepositoryImpl(session)
        register_agreement_service = AgreementService(agreement_repo, agreement_port)
        
        # Crear caso de uso
        use_case = AgreementUseCase(agreement_port, register_agreement_service)
        
        # Ejecutar caso de uso
        result = await use_case.execute(agreement.dict())
        
        return JSONResponse(content=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/agreement/{agreement_id}", response_model=dict, tags=["Agreement"])
async def get_agreement(agreement_id: int, session: AsyncSession = Depends(get_session)):
    try:
        agreement_repo = AgreementRepositoryImpl(session)
        agreement = await agreement_repo.find_by_id(agreement_id)
        
        if not agreement:
            raise HTTPException(status_code=404, detail="Acuerdo no encontrado")
        
        return JSONResponse(content={
            "id": agreement.id,
            "job_offer_id": agreement.job_offer_id,
            "student_id": agreement.student_id,
            "status": agreement.status.value,
            "start_date": agreement.start_date.isoformat() if agreement.start_date else None,
            "end_date": agreement.end_date.isoformat() if agreement.end_date else None
        })
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/student/{student_id}/agreements", response_model=dict, tags=["Agreement"])
async def get_student_agreements(student_id: int, session: AsyncSession = Depends(get_session)):
    try:
        agreement_repo = AgreementRepositoryImpl(session)
        agreements = await agreement_repo.find_by_student_id(student_id)
        
        agreements_data = []
        for agreement in agreements:
            agreements_data.append({
                "id": agreement.id,
                "job_offer_id": agreement.job_offer_id,
                "student_id": agreement.student_id,
                "status": agreement.status.value,
                "start_date": agreement.start_date.isoformat() if agreement.start_date else None,
                "end_date": agreement.end_date.isoformat() if agreement.end_date else None
            })
        
        return JSONResponse(content={"agreements": agreements_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/agreement/{agreement_id}", response_model=dict, tags=["Agreement"])
async def get_agreement_by_id(agreement_id: int, session: AsyncSession = Depends(get_session)):
    agreement_repo = AgreementRepositoryImpl(session)
    agreement = await agreement_repo.find_by_id(agreement_id)
    if not agreement:
        raise HTTPException(status_code=404, detail="Agreement not found")
    return agreement.__dict__

@router.get("/agreement/all", response_model=list, tags=["Agreement"])
async def get_all_agreements(session: AsyncSession = Depends(get_session)):
    agreement_repo = AgreementRepositoryImpl(session)
    agreements = await agreement_repo.get_all()
    return [a.__dict__ for a in agreements]

@router.put("/agreement/{agreement_id}", response_model=dict, tags=["Agreement"])
async def update_agreement(agreement_id: int, agreement: AgreementCreate, session: AsyncSession = Depends(get_session)):
    agreement_repo = AgreementRepositoryImpl(session)
    updated = await agreement_repo.update(agreement_id, agreement.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Agreement not found")
    return updated.__dict__

@router.delete("/agreement/{agreement_id}", response_model=dict, tags=["Agreement"])
async def delete_agreement(agreement_id: int, session: AsyncSession = Depends(get_session)):
    agreement_repo = AgreementRepositoryImpl(session)
    deleted = await agreement_repo.delete(agreement_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Agreement not found")
    return {"detail": "Agreement deleted"}
