from app.application.ports.match_job_student_port import MatchJobStudentPort
from app.domain.entities.student import Student
from app.domain.entities.job_offer import JobOffer
from typing import List

class MatchJobStudentUseCase:
    def __init__(self, match_job_student_port: MatchJobStudentPort):
        self.match_job_student_port = match_job_student_port

    async def match_job_student(self, student: Student, job_offers: List[JobOffer]):
        return await self.match_job_student_port.match_job_student(student, job_offers)

    async def match_student_job(self, job_offer: JobOffer, students: List[Student]):
        return await self.match_job_student_port.match_student_job(job_offer, students)