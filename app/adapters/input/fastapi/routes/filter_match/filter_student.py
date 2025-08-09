from typing import List
import logging
from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session

from app.adapters.input.fastapi.schemas.filter_match_schema import (FilterMatchCreate, FilterMatchResponse)
from app.application.factories.filter_match_factory import FilterMatchUseCaseFactory
from app.domain.entities.student import Student
from app.adapters.output.orm.repositories.student_repository_impl import StudentRepositoryImpl

router = APIRouter()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/filter/student/preprocess_all_student", response_model=List[FilterMatchResponse], tags=["AI Model"])
async def preprocess_all_student(session: AsyncSession = Depends(get_session)):
    use_case = FilterMatchUseCaseFactory(session).build()
    student_repo = StudentRepositoryImpl(session)
    students: List[Student] = await student_repo.get_all()
    student_ids = [st.id for st in students]
    try:
        processed = await use_case.preprocess_all_students(student_ids)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error en la API de IA: {str(e)}")
    # Filtrar duplicados por student_id y asegurar campos opcionales
    seen_ids = set()
    response_list = []
    for item in processed:
        item_id = item.get("student_id") or item.get("id")
        if item_id is not None and item_id in seen_ids:
            continue
        seen_ids.add(item_id)
        response_list.append(FilterMatchResponse(**item))
    return response_list

@router.post("/filter/student/preprocess_student", response_model=FilterMatchResponse, tags=["AI Model"])
async def preprocess_student(student_id: int = Body(..., embed=True), session: AsyncSession = Depends(get_session)):
    use_case = FilterMatchUseCaseFactory(session).build()
    student_repo = StudentRepositoryImpl(session)
    student = await student_repo.find_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    try:
        processed = await use_case.preprocess_student(student_id)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error en la API de IA: {str(e)}")
    if not processed:
        raise HTTPException(status_code=500, detail="No se pudo obtener el embedding")
    return FilterMatchResponse(**processed)