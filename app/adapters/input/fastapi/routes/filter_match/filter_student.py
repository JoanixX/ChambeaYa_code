from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session

from app.domain.repositories.student_repository import get_all_students, get_student_by_id
from app.domain.entities.student import Student
from typing import List
from fastapi import Body
from app.domain.services.preprocess_student_service import PreprocessStudentService

router = APIRouter()

@router.post("/filter/student/preprocess_all_student")
async def preprocess_all_student(session: AsyncSession = Depends(get_session)):
    students: List[Student] = await get_all_students(session)
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

@router.post("/filter/student/preprocess_student")
async def preprocess_student(student_id: int = Body(..., embed=True), session: AsyncSession = Depends(get_session)):
    student = await get_student_by_id(session, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student_data = {
        "id": student.id,
        "name": student.name,
        "email": student.email,
        "career": student.career,
        "academic_cycle": student.academic_cycle,
        "location": student.location,
        "main_motivation": student.main_motivation,
        "description": student.description,
        "weekly_availability": student.weekly_availability,
        "preferred_modality": student.preferred_modality,
        "experience_id": student.experience_id,
        "date_of_birth": student.date_of_birth.isoformat() if student.date_of_birth else None,
        "embedding": None
    }

    try:
        processed = await preprocess_all_student([student_data])
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