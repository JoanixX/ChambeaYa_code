# ai_connection.py
import os
import httpx

IA_API_BASE_URL = os.getenv("IA_API_URL", "http://localhost:8001")

async def preprocess_all_students(students_data):
    url = f"{IA_API_BASE_URL}/filter/student/preprocess_all_student"
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, json=students_data)
        response.raise_for_status()
        return response.json()

async def preprocess_student(student: dict):
    url = f"{IA_API_BASE_URL}/filter/student/preprocess_student"
    payload = {"id": student.get("id")}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        return response.json()

async def preprocess_all_job_offers():
    url = f"{IA_API_BASE_URL}/filter/job_offer/preprocess_all_job_offer"
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url)
        response.raise_for_status()
        return response.json()

async def preprocess_job_offer(job_offer: dict):
    url = f"{IA_API_BASE_URL}/filter/job_offer/preprocess_job_offer"
    payload = {"id": job_offer.get("id")}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        return response.json()

async def match_best_job_offers(student: dict, job_offers: list):
    url = f"{IA_API_BASE_URL}/aimodel/job_offer/api/best_job_offers"
    payload = {
        "student_id": student.get("id"),
        "job_offer_ids": [offer.get("id") for offer in job_offers]
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        return response.json()

async def match_best_students(job_offer: dict, students: list):
    url = f"{IA_API_BASE_URL}/aimodel/student/api/best_students"
    payload = {
        "job_offer_id": job_offer.get("id"),
        "student_ids": [s.get("id") for s in students]
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        return response.json()