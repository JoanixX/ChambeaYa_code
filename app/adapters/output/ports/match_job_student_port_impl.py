from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.domain.entities.match_job_student import MatchJobStudent
from app.adapters.output.orm.repositories.match_job_student_repository_impl import MatchJobStudentRepositoryImpl
from app.application.ports.match_job_student_port import MatchJobStudentPort

from app.adapters.output.orm.repositories.job_offer_repository_impl import JobOfferRepositoryImpl
from app.adapters.output.orm.repositories.student_repository_impl import StudentRepositoryImpl
from app.adapters.output.orm.repositories.filter_match_repository_impl import FilterMatchRepositoryImpl
from app.infraestructure.ai_client.ai_connection import match_best_job_offers, match_best_students

class MatchJobStudentPortImpl(MatchJobStudentPort):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.match_job_student_repo = MatchJobStudentRepositoryImpl(session)
        self.filter_match_repo = FilterMatchRepositoryImpl(session)

    async def register_match_job_student(self, match_job_student_data: Dict[str, Any]) -> MatchJobStudent:
        if 'match_date' not in match_job_student_data:
            match_job_student_data['match_date'] = datetime.now()
        if 'updated_at' not in match_job_student_data:
            match_job_student_data['updated_at'] = datetime.now()
        entity = MatchJobStudent(
            id=0,
            student_id=match_job_student_data["student_id"],
            job_offer_id=match_job_student_data["job_offer_id"],
            score=match_job_student_data["score"],
            match_date=match_job_student_data["match_date"],
            rank=match_job_student_data.get("rank", 1),
            updated_at=match_job_student_data["updated_at"],
            deleted_at=match_job_student_data.get("deleted_at")
        )
        # Guardar en la base de datos
        saved = await self.match_job_student_repo.save(entity)
        return saved

    async def match_job_student(self, student_id: int):
        student_repo = StudentRepositoryImpl(self.session)
        student = await student_repo.find_by_id(student_id)
        if not student or not student.embedding:
            raise ValueError("El estudiante no tiene embedding disponible")
        # Obtener todas las ofertas con embedding
        job_offer_repo = JobOfferRepositoryImpl(self.session)
        job_offers = await job_offer_repo.get_all()
        job_offers_with_embedding = [j for j in job_offers if j.embedding and j.id is not None]
        job_offer_payloads = [
            {"id": j.id, "embedding": j.embedding}
            for j in job_offers_with_embedding
        ]
        student_payload = {"id": student.id, "embedding": student.embedding}
        import logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        logger.info(f"Payload IA student: {student_payload}")
        logger.info(f"Payload IA job_offers: {job_offer_payloads}")
        ia_result = await match_best_job_offers(student_payload, job_offer_payloads)
        return ia_result

    async def match_student_job(self, job_offer_id: int):
        job_offer_repo = JobOfferRepositoryImpl(self.session)
        job_offer = await job_offer_repo.find_by_id(job_offer_id)
        if not job_offer or not job_offer.embedding:
            raise ValueError("La oferta no tiene embedding disponible")
        # Obtener todos los estudiantes con embedding
        student_repo = StudentRepositoryImpl(self.session)
        students = await student_repo.get_all()
        students_with_embedding = [s for s in students if s.embedding and s.id is not None]
        student_payloads = [
            {"id": s.id, "embedding": s.embedding}
            for s in students_with_embedding
        ]
        job_offer_payload = {"id": job_offer.id, "embedding": job_offer.embedding}
        import logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        logger.info(f"Payload IA job_offer: {job_offer_payload}")
        logger.info(f"Payload IA students: {student_payloads}")
        ia_result = await match_best_students(job_offer_payload, student_payloads)
        return ia_result