# ai_connection.py
import os
import httpx

IA_API_BASE_URL = os.getenv("IA_API_URL", "http://localhost:8001")

async def preprocess_all_students(students: list):
    url = f"{IA_API_BASE_URL}/filter/student/preprocess_all_student"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=students)
    response.raise_for_status()
    return response.json()

async def preprocess_all_job_offers(job_offers: list):
    url = f"{IA_API_BASE_URL}/filter/job_offer/preprocess_all_job_offer"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=job_offers)
    response.raise_for_status()
    return response.json()

async def match_best_job_offers(student: dict, job_offers: list):
    url = f"{IA_API_BASE_URL}/aimodel/student/best_job_offers"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={"student": student, "job_offers": job_offers})
    response.raise_for_status()
    return response.json()

async def match_best_students(job_offer: dict, students: list):
    url = f"{IA_API_BASE_URL}/aimodel/student/best_students"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={"job_offer": job_offer, "students": students})
    response.raise_for_status()
    return response.json()