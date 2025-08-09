from typing import List
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session

from app.adapters.input.fastapi.schemas.match_job_student_schema import (MatchJobStudentCreate, MatchJobStudentResponse)
from app.application.factories.match_job_student_factory import MatchJobStudentUseCaseFactory

router = APIRouter()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/aimodel/student/best_job_offers/{student_id}", response_model=List[MatchJobStudentResponse], tags=["AI Model"])
async def best_job_offers(student_id: int, session: AsyncSession = Depends(get_session)):
    use_case = MatchJobStudentUseCaseFactory(session).build()
    try:
        result = await use_case.match_job_students(student_id)
        logger.info(f"Respuesta IA: {result}")
        matches = result.get("matches", []) if isinstance(result, dict) else result
    except Exception as e:
        logger.error(f"Error en la API de IA: {str(e)}")
        raise HTTPException(status_code=502, detail=f"Error en la API de IA: {str(e)}")

    if not matches:
        logger.error("No se pudieron obtener las ofertas de trabajo")
        raise HTTPException(status_code=500, detail="No se pudieron obtener las ofertas de trabajo")

    for item in matches:
        if "id" not in item:
            item["id"] = None
    logger.info(f"Matches procesados: {matches}")
    return [MatchJobStudentResponse(**item) for item in matches]
