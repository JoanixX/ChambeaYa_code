from typing import Dict, List
import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session

from app.adapters.input.fastapi.schemas.agreement_schema import (AgreementCreate, AgreementResponse)
from app.application.factories.agreement_factory import AgreementUseCaseFactory

router = APIRouter()
# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/register/agreement", response_model=dict, tags=["Agreement"])
async def register_agreement(request: Request, agreement: AgreementCreate, session: AsyncSession = Depends(get_session)):
    try:
        body = await request.body()
        logger.info(f"Body recibido: {body.decode()}")

        agreement_use_case = AgreementUseCaseFactory(session).build()

        logger.info(f"Iniciando registro del acuerdo: {agreement.job_offer_id} para el estudiante: {agreement.student_id}")
        result = await agreement_use_case.register_agreement(agreement.dict())
        logger.info(f"Acuerdo registrado exitosamente: {result}")
        return JSONResponse(content=result)
    
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error al registrar el acuerdo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/agreement/all", response_model=list, tags=["Agreement"])
async def get_all_agreements(session: AsyncSession = Depends(get_session)):
    try:
        agreement_use_case = AgreementUseCaseFactory(session).build()
        agreements = await agreement_use_case.get_all_agreements()
        return [AgreementResponse(**a.__dict__).model_dump() for a in agreements]
    
    except Exception as e:
        logger.error(f"Error al obtener acuerdos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/agreement/{agreement_id}", response_model=dict, tags=["Agreement"])
async def get_agreement(agreement_id: int, session: AsyncSession = Depends(get_session)):
    try:
        agreement_use_case = AgreementUseCaseFactory(session).build()
        agreement = await agreement_use_case.get_agreement(agreement_id)
        return AgreementResponse(**agreement.__dict__).model_dump()
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error al obtener el acuerdo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/job_offer/{job_offer_id}/agreements", response_model=List[Dict], tags=["Agreement"])
async def get_job_offer_agreements(job_offer_id: int, session: AsyncSession = Depends(get_session)):
    try:
        agreement_use_case = AgreementUseCaseFactory(session).build()
        agreements = await agreement_use_case.get_job_offer_agreements(job_offer_id)
        return [AgreementResponse(**a.__dict__).model_dump() for a in agreements]
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error al obtener acuerdos de la oferta de trabajo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/student/{student_id}/agreements", response_model=List[Dict], tags=["Agreement"])
async def get_student_agreements(student_id: int, session: AsyncSession = Depends(get_session)):
    try:
        agreement_use_case = AgreementUseCaseFactory(session).build()
        agreements = await agreement_use_case.get_student_agreements(student_id)
        return [AgreementResponse(**a.__dict__).model_dump() for a in agreements]
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error al obtener acuerdos del estudiante: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.put("/agreement/{agreement_id}", response_model=dict, tags=["Agreement"])
async def update_agreement(agreement_id: int, agreement: AgreementCreate, session: AsyncSession = Depends(get_session)):
    try:
        agreement_use_case = AgreementUseCaseFactory(session).build()
        updated_agreement = await agreement_use_case.update_agreement(agreement_id, agreement.dict())
        return AgreementResponse(**updated_agreement.__dict__).model_dump()
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error al actualizar acuerdo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.delete("/agreement/{agreement_id}", response_model=dict, tags=["Agreement"])
async def delete_agreement(agreement_id: int, session: AsyncSession = Depends(get_session)):
    try:
        agreement_use_case = AgreementUseCaseFactory(session).build()
        deleted_agreement = await agreement_use_case.delete_agreement(agreement_id)
        return deleted_agreement
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error al eliminar acuerdo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")