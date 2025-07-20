from app.domain.entities.job_offer import JobOffer
from app.domain.repositories.match_job_student_repository import MatchJobStudentRepository
from app.application.ports.create_match_port import CreateMatchPort
from app.domain.entities.match_job_student import MatchJobStudent
from app.domain.entities.student import Student

class MatchJobStudentService:
    def __init__(self, match_js_repo: MatchJobStudentRepository, match_js_port: CreateMatchPort):
        self.match_js_repo = match_js_repo
        self.match_js_port = match_js_port

    async def matching_model(self, student: Student, job_offer: JobOffer):
        result = await self.match_js_port.match_job_student(student, job_offer)
        
        match_job_student = MatchJobStudent(
            match_job_student_id=result["id"],
            student_id=result["student_id"],
            job_offer_id=result["job_offer_id"],
            score=result["score"],
            match_date=result["match_date"],
            rank=result["rank"]
        )

        await self.match_js_repo.save(match_job_student)
        return match_job_student