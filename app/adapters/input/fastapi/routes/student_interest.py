from typing import List
import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session

from app.domain.entities.student_interest import StudentInterest
from app.adapters.input.fastapi.schemas.student_interest_schema import (StudentInterestResponse, StudentInterestCreate)
from app.application.factories.student_interest_factory import StudentInterestUseCaseFactory

router = APIRouter()
# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
    
@router.post("/student/student_interest", response_model=StudentInterestResponse, tags=["Student", "Interest"])
async def add_student_interest(request: Request, student_interest: StudentInterestCreate, session: AsyncSession = Depends(get_session)):
    try:
        student_interest_use_case = StudentInterestUseCaseFactory(session).build()

        student_interest  = StudentInterest(
            student_id=student_interest.student_id,
            interest_id=student_interest.interest_id
        )

        result = await student_interest_use_case.add_student_interest(student_interest)
        return StudentInterestResponse(student_id=result.student_id, interest_id=result.interest_id)
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error al agregar interests al estudiante: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/student/{student_id}/interests", response_model=List[StudentInterestResponse], tags=["Student", "Interest"])
async def get_student_interests(student_id: int, session: AsyncSession = Depends(get_session)):
    try:
        student_interest_use_case = StudentInterestUseCaseFactory(session).build()

        interests = await student_interest_use_case.get_student_interests(student_id)
        return [interest.__dict__ for interest in interests]
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
@router.delete("/student/{student_id}/interest/{interest_id}", response_model=dict, tags=["Student", "Interest"])
async def delete_student_interest(student_id: int, interest_id: int, session: AsyncSession = Depends(get_session)):
    try:
        student_interest_use_case = StudentInterestUseCaseFactory(session).build()
        deleted = await student_interest_use_case.delete_student_interest(student_id, interest_id)

        return deleted
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")