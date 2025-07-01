from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.infraestructure.database.connection import get_session
from app.domain.entities.student import Student
from app.domain.entities.job_offer import JobOffer
from app.infraestructure.ai_client.ai_connection import match_best_job_offers

router = APIRouter()

@router.post("/aimodel/student/best_job_offers/{student_id}")
async def best_job_offers(student_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()

    if student is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    student_data = {
        "id": student.id,
        "name": student.name,
        "email": student.email,
        "career": student.career,
        "description": student.description,
        "weekly_availability": student.weekly_availability,
        "preferred_modality": student.preferred_modality,
        "experience_id": student.experience_id,
        "date_of_birth": student.date_of_birth.isoformat() if student.date_of_birth else None,
        "skills": [],
        "interests": [],
        "embedding": student.embedding
    }


    result = await session.execute(select(JobOffer).where(JobOffer.embedding.is_not(None)))
    job_offers = result.scalars().all()

    job_offers_data = []
    for j in job_offers:
        job_offers_data.append({
            "id": j.id,
            "title": j.title,
            "description": j.description,
            "required_hours": j.required_hours,
            "approximated_salary": j.approximated_salary,
            "duration": j.duration,
            "start_date": j.start_date.isoformat() if j.start_date else None,
            "area_id": j.area_id,
            "experience_id": j.experience_id,
            "modality": j.modality,
            "required_skills": [],
            "embedding": j.embedding
        })

    try:
        response = await match_best_job_offers(student_data, job_offers_data)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error en la API de IA: {str(e)}")

    return response.json()
