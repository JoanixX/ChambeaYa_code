import requests

def call_filter_match_ia(job_offer: dict):
    url = "http://localhost:8001/filter/preprocess_job_offer"
    response = requests.post(url, json=job_offer)
    response.raise_for_status()
    return response.json()

def call_match_job_student_ia(estudiante: dict, job_offer: dict):
    url = "http://localhost:8001/aimodel/match_job_student"
    payload = {
        "estudiante": estudiante,
        "job_offer": job_offer
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()