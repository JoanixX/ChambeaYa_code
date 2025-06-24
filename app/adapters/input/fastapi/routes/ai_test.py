from fastapi import APIRouter
import requests
from pydantic import BaseModel

router = APIRouter()

class KawsAIClass(BaseModel):
    career: str
    habilidades_destacadas: str
    areas_interes: str
    description: str
    experience_id: str
    preferred_modality: int
    weekly_availability: int

@router.get("/test-ai-connection/")
def test_ai_connection():
    estudiante_prueba = KawsAIClass(
        career="Medicina",
        habilidades_destacadas="Tomar Presión, Diagnosticar Enfermedades",
        areas_interes="Neurología, Neurocirugía",
        description="Estudiante de medicina con interés en neurología y neurocirugía.",
        experience_id="Cuidar a familiares enfermos",
        preferred_modality=1,
        weekly_availability=30
    )
    try:
        response = requests.get(
            "http://localhost:8001/test_match/",
            json=estudiante_prueba.dict()
        )
        response.raise_for_status()
        return {"respuesta": response.json()}
    except Exception as e:
        detalle = str(getattr(e, 'response', ''))
        return {"error": str(e), "detalle": detalle}
