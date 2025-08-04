from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session
from app.adapters.output.orm.repositories.student_repository_impl import StudentRepositoryImpl
from app.domain.entities.student import Student
from app.adapters.input.fastapi.schemas.filter_match_schema import FilterMatchStudentResponse
from typing import List
from fastapi import Body
from app.domain.services.filter_match_service import FilterMatchService
from app.adapters.output.orm.repositories.filter_match_repository_impl import FilterMatchRepositoryImpl
from sqlalchemy.future import select
from app.adapters.output.orm.models.student_model import StudentModel

router = APIRouter()

from app.application.factories.filter_match_factory import FilterMatchUseCaseFactory


@router.post("/filter/student/preprocess_all_student", response_model=List[FilterMatchStudentResponse], tags=["AI Model"])
async def preprocess_all_student(session: AsyncSession = Depends(get_session)):
    use_case = FilterMatchUseCaseFactory.create(session)
    service = FilterMatchService(FilterMatchRepositoryImpl(session), session)
    student_repo = StudentRepositoryImpl(session)
    students: List[Student] = await student_repo.get_all()
    student_ids = [st.id for st in students]
    try:
        processed = await service.preprocess_all_students(student_ids)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error en la API de IA: {str(e)}")
    return [FilterMatchStudentResponse(**item).model_dump() for item in processed]


@router.post("/filter/student/preprocess_student", response_model=FilterMatchStudentResponse, tags=["AI Model"])
async def preprocess_student(student_id: int = Body(..., embed=True), session: AsyncSession = Depends(get_session)):
    use_case = FilterMatchUseCaseFactory.create(session)
    service = FilterMatchService(FilterMatchRepositoryImpl(session), session)
    student_repo = StudentRepositoryImpl(session)
    student = await student_repo.find_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    try:
        processed = await service.preprocess_student(student_id)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error en la API de IA: {str(e)}")
    if not processed:
        raise HTTPException(status_code=500, detail="No se pudo obtener el embedding")
    return FilterMatchStudentResponse(**processed)