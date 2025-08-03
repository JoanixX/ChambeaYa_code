from typing import List
import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session

from app.adapters.input.fastapi.schemas.student_schema import (StudentCreate, StudentResponse)
from app.application.factories.student_factory import StudentUseCaseFactory

router = APIRouter()
# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/register/student", response_model=dict, tags=["Estudiante"])
async def register_student(request: Request, student: StudentCreate, session: AsyncSession = Depends(get_session)):
    try:
        body = await request.body()
        logger.info(f"Body recibido: {body.decode()}")
        logger.info(f"Iniciando registro de estudiante: {student.email}")
        
        student_use_case = StudentUseCaseFactory(session).build()

        logger.info("Ejecutando caso de uso...")
        result = await student_use_case.register_student(student.dict())
        
        logger.info(f"Estudiante registrado exitosamente: {result}")
        return JSONResponse(content=result)
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error interno del servidor: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/student/all", response_model=List[dict], tags=["Estudiante"])
async def get_all_students(session: AsyncSession = Depends(get_session)):
    try:
        student_use_case = StudentUseCaseFactory(session).build()
        students = await student_use_case.get_all_students()

        def serialize_student(s):
            d = s.__dict__.copy()
            if d.get("date_of_birth"):
                d["date_of_birth"] = d["date_of_birth"].isoformat()
            return d

        return [serialize_student(s) for s in students]
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/student/{student_id}", response_model=dict, tags=["Estudiante"])
async def get_student_by_id(student_id: int, session: AsyncSession = Depends(get_session)):
    try:
        student_use_case = StudentUseCaseFactory(session).build()
        student = await student_use_case.get_student(student_id)

        return student.__dict__
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.put("/student/{student_id}", response_model=dict, tags=["Estudiante"])
async def update_student(student_id: int, student: StudentCreate, session: AsyncSession = Depends(get_session)):
    try:
        student_use_case = StudentUseCaseFactory(session).build()
        updated_student = await student_use_case.update_student(student_id, student.dict())

        return updated_student.__dict__
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.delete("/student/{student_id}", response_model=dict, tags=["Estudiante"])
async def delete_student(student_id: int, session: AsyncSession = Depends(get_session)):
    try:
        student_use_case = StudentUseCaseFactory(session).build()
        result = await student_use_case.delete_student(student_id)

        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")