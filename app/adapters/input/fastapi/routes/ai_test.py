# from fastapi import APIRouter
# import requests
# from pydantic import BaseModel

# router = APIRouter()

# class KawsAIClass(BaseModel):
#     career: str
#     habilidades_destacadas: str
#     areas_interes: str
#     description: str
#     experience_id: str
#     preferred_modality: int
#     weekly_availability: int

# @router.get("/test-ai-connection/")
# def test_ai_connection():
#     estudiante_prueba = KawsAIClass(
#         career="Ingeniería de Sistemas",
#         habilidades_destacadas="Programación en Python, Desarrollo Web, Análisis de Datos",
#         areas_interes="Inteligencia Artificial, Ciberseguridad",
#         description="Estudiante de ingeniería de sistemas apasionado por la tecnología, con enfoque en IA y seguridad informática.",
#         experience_id="Proyectos universitarios de software y prácticas en empresas tecnológicas",
#         preferred_modality=2,
#         weekly_availability=20
#     )
#     try:
#         response = requests.post(
#             "http://localhost:8001/test_match/",
#             json=estudiante_prueba.dict()
#         )
#         response.raise_for_status()
#         return {"respuesta": response.json()}
#     except Exception as e:
#         detalle = str(getattr(e, 'response', ''))
#         return {"error": str(e), "detalle": detalle}
