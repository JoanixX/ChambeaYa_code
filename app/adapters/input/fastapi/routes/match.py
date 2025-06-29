# match.py
# Endpoint para obtener los mejores matches entre un estudiante y las ofertas de trabajo.
# Recibe solo el estudiante_id, arma el payload, llama a la IA para obtener embeddings,
# calcula la distancia entre el estudiante y cada oferta, y devuelve los 3 mejores matches.

from fastapi import APIRouter, Body, Depends
from sqlalchemy.future import select
from sqlalchemy import text
from app.infraestructure.database.connection import get_session
from app.domain.entities.student import Student
from app.domain.entities.job_offer import JobOffer
from app.infraestructure.ai_client.ai_connection import call_preprocess_all_job_offers

router = APIRouter()

@router.post("/match-job-student/")
async def match_job_student(payload: dict = Body(...), session=Depends(get_session)):
    # 1. Recibe solo el estudiante_id en el body
    estudiante_id = payload.get("estudiante_id")
    if not estudiante_id:
        return {"error": "Debes enviar 'estudiante_id' en el body"}
    # 2. Busca el estudiante en la base de datos
    result = await session.execute(select(Student).where(Student.id == estudiante_id))
    estudiante = result.scalar_one_or_none()
    if not estudiante:
        return {"error": f"No se encontró el estudiante con id {estudiante_id}"}
    # 3. Obtiene las habilidades (skills) y los intereses (interests) del estudiante
    skills_result = await session.execute(text("SELECT skill_id FROM student_skill WHERE student_id = :id"), {"id": estudiante_id})
    habilidades_destacadas = [row[0] for row in skills_result.fetchall()]
    interests_result = await session.execute(text("SELECT interest_id FROM student_interest WHERE student_id = :id"), {"id": estudiante_id})
    areas_interes = [row[0] for row in interests_result.fetchall()]
    # 4. Arma el diccionario del estudiante con los campos requeridos por la IA
    estudiante_dict = {
        "id": estudiante.id,
        "career": estudiante.career,
        "habilidades_destacadas": habilidades_destacadas,
        "areas_interes": areas_interes,
        "description": estudiante.description,
        "experience_id": estudiante.experience_id
    }
    # 5. Busca todas las ofertas de trabajo y arma el diccionario de cada una
    result = await session.execute(select(JobOffer))
    offers = result.scalars().all()
    job_offers = []
    offer_map = {}
    for offer in offers:
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
        offer_map[offer.id] = offer_dict
    # 6. Llama al microservicio de IA para obtener los embeddings de estudiante y ofertas
    ia_response = call_preprocess_all_job_offers(estudiante_dict, job_offers)
    from scipy.spatial.distance import cosine
    estudiante_emb = ia_response["estudiante"]["embedding"]
    matches = []
    # 7. Calcula la distancia (similitud) entre el embedding del estudiante y cada oferta
    for offer in ia_response["job_offers"]:
        job_emb = offer["embedding"]
        dist = cosine(estudiante_emb, job_emb)
        # Junta los datos principales de la oferta y la distancia
        offer_info = offer_map.get(offer["id"], {})
        matches.append({**offer_info, "distancia": dist})
    # 8. Ordena por distancia y limita a los 3 mejores matches
    matches_sorted = sorted(matches, key=lambda x: x["distancia"])[:3]
    # 9. Devuelve solo los 3 mejores matches y los datos del estudiante
    return {
        "estudiante": estudiante_dict,
        "matches": matches_sorted
    }