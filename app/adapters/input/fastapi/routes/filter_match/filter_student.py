from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session

from app.adapters.output.orm.repositories.student_repository_impl import StudentRepositoryImpl
from app.domain.entities.student import Student
from typing import List
from fastapi import Body
from app.domain.services.preprocess_student_service import PreprocessStudentService

router = APIRouter()

@router.post("/filter/student/preprocess_all_student", response_model=dict, tags=["AI Model"])
async def preprocess_all_student(session: AsyncSession = Depends(get_session)):
    repo = StudentRepositoryImpl(session)
    students: List[Student] = await repo.get_all()
    service = PreprocessStudentService()
    try:
        processed = await service.preprocess_all(students)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error en la API de IA: {str(e)}")

    id_to_embedding = {item["student_id"]: item["embedding"] for item in processed}

    for student in students:
        embedding = id_to_embedding.get(student.id)
        if embedding:
            student.embedding = embedding

    await session.commit()
    return {"message": "Embedding generado y guardado correctamente", "total": len(students)}

@router.post("/filter/student/preprocess_student", response_model=dict, tags=["AI Model"])
async def preprocess_student(student_id: int = Body(..., embed=True), session: AsyncSession = Depends(get_session)):
    repo = StudentRepositoryImpl(session)
    student = await repo.find_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    service = PreprocessStudentService()
    try:
        processed = await service.preprocess_student(student)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error en la API de IA: {str(e)}")

    embedding = None
    if processed and isinstance(processed, list) and len(processed) > 0:
        embedding = processed[0].get("embedding")
    if embedding is None:
        raise HTTPException(status_code=500, detail="No se pudo obtener el embedding")

    student.embedding = embedding
    await session.commit()
    return {"message": "Embedding generado y guardado correctamente", "student_id": student.id}