from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from app.infraestructure.database.connection import get_session
from app.domain.repositories.student_repository import get_all_students
from app.domain.entities.student import Student
from typing import List
import httpx
import os

router = APIRouter()

IA_API_URL_STUDENT = os.getenv("IA_API_URL", "http://localhost:8001/filter/student/preprocess_all_student")

@router.post("/filter/student/preprocess_all_student")
async def preprocess_all_student(session: AsyncSession = Depends(get_session)):
    students: List[Student] = await get_all_students(session)
    students_data = []
    for s in students:
        students_data.append({
            "id": s.id,
            "name": s.name,
            "email": s.email,
            "career": s.career,
            "academic_cycle": s.academic_cycle,
            "location": s.location,
            "main_motivation": s.main_motivation,
            "description": s.description,
            "weekly_availability": s.weekly_availability,
            "preferred_modality": s.preferred_modality,
            "experience_id": s.experience_id,
            "date_of_birth": s.date_of_birth.isoformat() if s.date_of_birth else None,
            "embedding": None
        })

    async with httpx.AsyncClient() as client:
        response = await client.post(IA_API_URL_STUDENT, json=students_data)
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Error en la API de IA")
    embeddings = response.json().get("embeddings")
    if not embeddings or len(embeddings) != len(students):
        raise HTTPException(status_code=500, detail="Embeddings no válidos")

    for student, embedding in zip(students, embeddings):
        await session.execute(
            update(Student)
            .where(Student.id == student.id)
            .values(embedding=embedding)
        )
    await session.commit()
    return {"status": "ok", "updated": len(students)}