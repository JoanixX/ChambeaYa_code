from app.domain.entities.job_offer import JobOffer
from app.domain.repositories.match_job_student_repository import MatchJobStudentRepository
from app.application.ports.match_job_student_port import MatchJobStudentPort
from app.domain.entities.student import Student
from app.infraestructure.ai_client.ai_connection import match_best_job_offers, match_best_students
from typing import List

class MatchJobStudentService:
    def __init__(self, match_js_repo: MatchJobStudentRepository, match_js_port: MatchJobStudentPort, session=None):
        self.match_js_repo = match_js_repo
        self.match_js_port = match_js_port
        self.session = session

    async def match_best_from_student(self, student: Student, job_offers: List[JobOffer]):
        if not student.embedding:
            raise ValueError("El estudiante no tiene embedding. Debe preprocesarse primero.")
        offers_dicts = []
        for offer in job_offers:
            if not offer.embedding:
                raise ValueError(f"La oferta {offer.id} no tiene embedding. Debe preprocesarse primero.")
            offers_dicts.append({"id": offer.id, "embedding": offer.embedding})
        student_dict = {"id": student.id, "embedding": student.embedding}
        return await match_best_job_offers(student_dict, offers_dicts)

    async def match_best_from_offer(self, job_offer: JobOffer, students: List[Student]):
        if not job_offer.embedding:
            raise ValueError("La oferta no tiene embedding. Debe preprocesarse primero.")
        students_dicts = []
        for student in students:
            if not student.embedding:
                raise ValueError(f"El estudiante {student.id} no tiene embedding. Debe preprocesarse primero.")
            students_dicts.append({"id": student.id, "embedding": student.embedding})
        offer_dict = {"id": job_offer.id, "embedding": job_offer.embedding}
        return await match_best_students(offer_dict, students_dicts)