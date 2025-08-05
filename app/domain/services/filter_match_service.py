from typing import Any, Optional, List
from app.domain.repositories.filter_match_repository import FilterMatchRepository
from app.adapters.output.orm.repositories.job_offer_repository_impl import JobOfferRepositoryImpl
from app.adapters.output.orm.repositories.area_repository_impl import get_area_name_by_id_impl
from app.adapters.output.orm.repositories.experience_detail_repository_impl import get_experience_detail_by_id_impl
from app.adapters.output.orm.repositories.job_offer_required_skill_repository_impl import JobOfferRequiredSkillRepositoryImpl
from app.adapters.output.orm.repositories.skill_repository_impl import SkillRepositoryImpl
from app.infraestructure.ai_client.ai_connection import preprocess_all_job_offers
from app.adapters.output.orm.repositories.student_skill_repository_impl import StudentSkillRepositoryImpl
from app.adapters.output.orm.repositories.skill_repository_impl import SkillRepositoryImpl
from app.adapters.output.orm.repositories.student_interest_repository_impl import StudentInterestRepositoryImpl
from app.adapters.output.orm.repositories.interest_repository_impl import InterestRepositoryImpl
from sqlalchemy.ext.asyncio import AsyncSession

class FilterMatchService:
    def __init__(self, filter_match_repo: FilterMatchRepository, session: AsyncSession):
        self.filter_match_repo = filter_match_repo
        self.session = session

    async def preprocess_all_job_offers(self, job_offer_ids: List[int]) -> List[dict]:
        # 1. Obtener solo las ofertas válidas
        job_offer_repo = JobOfferRepositoryImpl(self.session)
        offers = []
        for oid in job_offer_ids:
            offer = await job_offer_repo.find_by_id(oid)
            if offer:
                offers.append(offer)
        if not offers:
            return []
        # 2. Preparar dicts completos
        dicts = []
        for offer in offers:
            area = await get_area_name_by_id_impl(self.session, offer.area_id) if offer.area_id else None
            required_skills = await JobOfferRequiredSkillRepositoryImpl(self.session).get_by_job_offer_id(offer.id)
            skill_names = []
            for req_skill in required_skills:
                skill = await SkillRepositoryImpl(self.session).find_by_id(req_skill.skill_id)
                if skill:
                    skill_names.append(skill.name)

            dicts.append({
                "id": offer.id,
                "title": offer.title,
                "description": offer.description,
                "area_id": area,
                "required_skills": skill_names,
                "embedding": None
            })
        # 3. Llamar a IA
        embeddings = await preprocess_all_job_offers(dicts)
        # 4. Guardar embeddings en la base de datos solo para los válidos
        for offer, emb in zip(offers, embeddings):
            if emb and "embedding" in emb:
                offer.embedding = emb["embedding"]
                await job_offer_repo.update(offer)
        # 5. Devolver solo los dicts válidos (con id y embedding)
        return [
            {"job_offer_id": emb.get("id"), "status": "processed", "stage": 1}
            for emb in embeddings if emb and emb.get("embedding") is not None
        ]

    async def preprocess_job_offer(self, job_offer_id: int) -> Optional[dict]:
        # Obtener la oferta válida
        job_offer_repo = JobOfferRepositoryImpl(self.session)
        offer = await job_offer_repo.find_by_id(job_offer_id)
        if not offer:
            return None
        import logging
        area = await get_area_name_by_id_impl(self.session, offer.area_id) if offer.area_id else None
        required_skills = await JobOfferRequiredSkillRepositoryImpl(self.session).get_by_job_offer_id(offer.id)
        skill_names = []
        for req_skill in required_skills:
            skill = await SkillRepositoryImpl(self.session).find_by_id(req_skill.skill_id)
            if skill:
                skill_names.append(skill.name)
        offer_dict = {
            "id": offer.id,
            "title": offer.title,
            "description": offer.description,
            "area_id": area,
            "required_skills": skill_names,
            "embedding": None
        }
        logging.warning(f"[PREPROCESS JOB_OFFER] Datos enviados: {offer_dict}")
        # Llamar a IA
        embeddings = await preprocess_all_job_offers([offer_dict])
        if embeddings and embeddings[0] and "embedding" in embeddings[0]:
            offer.embedding = embeddings[0]["embedding"]
            await job_offer_repo.update(offer)
            return {"job_offer_id": offer.id, "status": "processed", "stage": 1}
        return None

    async def preprocess_all_students(self, student_ids: List[int]) -> List[dict]:
        # 1. Obtener solo los estudiantes válidos
        from app.adapters.output.orm.repositories.student_repository_impl import StudentRepositoryImpl
        student_repo = StudentRepositoryImpl(self.session)
        students = []
        for sid in student_ids:
            student = await student_repo.find_by_id(sid)
            if student:
                students.append(student)
        if not students:
            return []
        # 2. Preparar dicts completos (ajusta los campos según tu modelo de estudiante)
        dicts = []
        skill_repo = StudentSkillRepositoryImpl(self.session)
        skill_name_repo = SkillRepositoryImpl(self.session)
        interest_repo = StudentInterestRepositoryImpl(self.session)
        interest_name_repo = InterestRepositoryImpl(self.session)
        
        for student in students:
            # Obtener skills
            student_skills = await skill_repo.get_by_student_id(student.id)
            skill_names = []
            for ss in student_skills:
                skill = await skill_name_repo.find_by_id(ss.skill_id)
                if skill:
                    skill_names.append(skill.name)
            # Obtener interests
            student_interests = await interest_repo.get_by_student_id(student.id)
            interest_names = []
            for si in student_interests:
                interest = await interest_name_repo.find_by_id(si.interest_id)
                if interest:
                    interest_names.append(interest.name)
            experience = await get_experience_detail_by_id_impl(self.session, student.experience_id) if getattr(student, 'experience_id', None) else None
            experience_str = f"{experience.name} {experience.description}" if experience else None
            dicts.append({
                "id": student.id,
                "career": student.career,
                "skills": skill_names,
                "interests": interest_names,
                "description": student.description,
                "experience_id": experience_str,
                "embedding": None
            })
        # 3. Llamar a IA
        from app.infraestructure.ai_client.ai_connection import preprocess_all_students
        embeddings = await preprocess_all_students(dicts)
        # 4. Guardar embeddings en la base de datos solo para los válidos
        for student, emb in zip(students, embeddings):
            if emb and "embedding" in emb:
                student.embedding = emb["embedding"]
                await student_repo.update(student)
        # 5. Devolver solo los dicts válidos (con id y embedding)
        return [
            {"student_id": emb.get("id"), "status": "processed", "stage": 1}
            for emb in embeddings if emb and emb.get("embedding") is not None
        ]

    async def preprocess_student(self, student_id: int) -> Optional[dict]:
        from app.adapters.output.orm.repositories.student_repository_impl import StudentRepositoryImpl
        student_repo = StudentRepositoryImpl(self.session)
        student = await student_repo.find_by_id(student_id)
        if not student:
            return None
        # Preparar dict completo
        skill_repo = StudentSkillRepositoryImpl(self.session)
        skill_name_repo = SkillRepositoryImpl(self.session)
        interest_repo = StudentInterestRepositoryImpl(self.session)
        interest_name_repo = InterestRepositoryImpl(self.session)
        # Obtener skills
        student_skills = await skill_repo.get_by_student_id(student.id)
        skill_names = []
        for ss in student_skills:
            skill = await skill_name_repo.find_by_id(ss.skill_id)
            if skill:
                skill_names.append(skill.name)
        # Obtener interests
        student_interests = await interest_repo.get_by_student_id(student.id)
        interest_names = []
        for si in student_interests:
            interest = await interest_name_repo.find_by_id(si.interest_id)
            if interest:
                interest_names.append(interest.name)
        import logging
        experience = await get_experience_detail_by_id_impl(self.session, student.experience_id) if getattr(student, 'experience_id', None) else None
        experience_str = f"{experience.name} {experience.description}" if experience else None
        student_dict = {
            "id": student.id,
            "career": student.career,
            "skills": skill_names,
            "interests": interest_names,
            "description": student.description,
            "experience_id": experience_str,
            "embedding": None
        }
        logging.warning(f"[PREPROCESS STUDENT] Datos enviados: {student_dict}")
        # Llamar a IA
        from app.infraestructure.ai_client.ai_connection import preprocess_all_students
        embeddings = await preprocess_all_students([student_dict])
        if embeddings and embeddings[0] and "embedding" in embeddings[0]:
            student.embedding = embeddings[0]["embedding"]
            await student_repo.update(student)
            return {"student_id": student.id, "status": "processed", "stage": 1}
        return None

    def _to_response_dict(self, data: Any) -> dict:
        if data is None:
            return {}

        if isinstance(data, dict):
            return data
        
        return {
            "job_offer_id": getattr(data, "job_offer_id", None),
            "student_id": getattr(data, "student_id", None),
            "status": getattr(data, "status", None),
            "stage": getattr(data, "stage", None)
        }
