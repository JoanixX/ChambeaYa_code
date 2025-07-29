from app.domain.entities.job_offer import JobOffer
from app.domain.repositories.match_job_student_repository import MatchJobStudentRepository
from app.application.ports.match_job_student_port import CreateMatchPort
from app.domain.entities.student import Student
from app.infraestructure.ai_client.ai_connection import match_best_job_offers, match_best_students
from typing import List

class MatchJobStudentService:
    def __init__(self, match_js_repo: MatchJobStudentRepository, match_js_port: CreateMatchPort):
        self.match_js_repo = match_js_repo
        self.match_js_port = match_js_port

    async def match_best(self, student: Student, job_offers: List[JobOffer]):
        student_data = {...}
        job_offers_data = [{...} for job in job_offers]
        return await match_best_job_offers(student_data, job_offers_data)

    async def match_best_from_offer(self, job_offer: JobOffer, students: List[Student]):
        job_offer_data = {...}
        students_data = [{...} for s in students]
        return await match_best_students(job_offer_data, students_data)