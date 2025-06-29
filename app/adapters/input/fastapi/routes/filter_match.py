# filter_match.py
# Endpoint para preprocesar los datos de un estudiante y todas las ofertas de trabajo,
# y enviar el payload completo al microservicio de IA para obtener los embeddings.
# El usuario solo envía el estudiante_id, el backend arma todo el JSON necesario.

from fastapi import APIRouter, Body, Depends
from sqlalchemy.future import select
from sqlalchemy import text
from app.infraestructure.database.connection import get_session
from app.domain.entities.student import Student
from app.domain.entities.job_offer import JobOffer
from app.infraestructure.ai_client.ai_connection import call_preprocess_all_job_offers

router = APIRouter()

@router.post("/filter-preprocess/")
async def filter_preprocess(payload: dict = Body(...), session=Depends(get_session)):
    # 1. Recibe solo el estudiante_id en el body
    estudiante_id = payload.get("estudiante_id")
    if not estudiante_id:
        return {"error": "Debes enviar 'estudiante_id' en el body"}
    # 2. Busca el estudiante en la base de datos
    result = await session.execute(select(Student).where(Student.id == estudiante_id))
    estudiante = result.scalar_one_or_none()
    if not estudiante:
        return {"error": f"No se encontró el estudiante con id {estudiante_id}"}
    # 3. Obtiene las habilidades (skills) del estudiante desde la tabla relacional student_skill
    skills_result = await session.execute(text("SELECT skill_id FROM student_skill WHERE student_id = :id"), {"id": estudiante_id})
    habilidades_destacadas = [row[0] for row in skills_result.fetchall()]
    # 4. Obtiene los intereses (interests) del estudiante desde la tabla relacional student_interest
    interests_result = await session.execute(text("SELECT interest_id FROM student_interest WHERE student_id = :id"), {"id": estudiante_id})
    areas_interes = [row[0] for row in interests_result.fetchall()]
    # 5. Arma el diccionario del estudiante con todos los campos requeridos por la IA
    estudiante_dict = {
        "id": estudiante.id,
        "career": estudiante.career,
        "habilidades_destacadas": habilidades_destacadas,
        "areas_interes": areas_interes,
        "description": estudiante.description,
        "experience_id": estudiante.experience_id
    }
    # 6. Busca todas las ofertas de trabajo en la base de datos
    result = await session.execute(select(JobOffer))
    offers = result.scalars().all()
    job_offers = []
    for offer in offers:
        # 7. Arma el diccionario de cada oferta con los campos requeridos por la IA
        offer_dict = {
            "id": offer.id,
            "title": offer.title,
            "description": offer.description,
            "required_hours": offer.required_hours,
            "approximated_salary": offer.approximated_salary,
            "duration": offer.duration,
            "start_date": offer.start_date.isoformat() if offer.start_date else None,
            "area_id": offer.area_id,
            "experience_id": offer.experience_id,
            "modality": offer.modality,
            "requirements": offer.requirements or ""
        }
        job_offers.append(offer_dict)
    # 8. Llama al microservicio de IA, enviando el estudiante y todas las ofertas
    #    El microservicio devuelve los embeddings para el estudiante y cada oferta
    return call_preprocess_all_job_offers(estudiante_dict, job_offers)