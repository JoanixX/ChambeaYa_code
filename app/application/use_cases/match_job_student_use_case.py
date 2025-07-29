from app.domain.entities.filter_match import FilterMatch
from app.application.ports.match_job_student_port import CreateMatchPort
from app.domain.entities.student import Student
from app.domain.entities.job_offer import JobOffer
from typing import List, Dict

class CreateMatchUseCase:
    def __init__(self, createMatchUseCase: CreateMatchPort):
        self.createMatchUseCase = createMatchUseCase

    async def match_job_student(self, student: Student, job_offers: List[JobOffer]):
        return await self.createMatchUseCase.match_job_student(student, job_offers)
    
    async def match_student_job(self, job_offer: JobOffer, students: List[Student]):
        return await self.createMatchUseCase.match_student_job(job_offer, students)