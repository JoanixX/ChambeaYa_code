# ai_connection.py
# Cliente HTTP para comunicarse con el microservicio de IA.
# Proporciona funciones para enviar datos de estudiantes y ofertas de trabajo,
# y recibir los embeddings o resultados de matching desde la IA.

import requests

# Llama al endpoint de la IA que preprocesa el estudiante y todas las ofertas de trabajo.
# Envía el estudiante y la lista de ofertas, y recibe los embeddings de ambos.
def call_preprocess_all_job_offers(estudiante: dict, job_offers: list):
    url = "http://localhost:8001/filter/preprocess_all_job_offers/"
    payload = {"estudiante": estudiante, "job_offers": job_offers}
    response = requests.post(url, json=payload)
    response.raise_for_status()  # Lanza excepción si la IA responde con error
    return response.json()       # Devuelve el JSON con los embeddings

# Llama al endpoint de la IA que realiza el matching entre estudiante y ofertas.
# Envía el estudiante y la lista de ofertas, y recibe el resultado del modelo de matching.
def call_match_job_student_ia(job_offers: list, estudiante: dict):
    url = "http://localhost:8001/aimodel/match_job_student"
    payload = {"job_offers": job_offers, "estudiante": estudiante}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()