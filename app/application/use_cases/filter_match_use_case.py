from typing import List

from app.application.ports.filter_match_port import FilterMatchPort
from app.domain.services.filter_match_service import FilterMatchService
from app.domain.entities.filter_match import FilterMatch

class FilterMatchUseCase:
    def __init__(self, filter_match_port: FilterMatchPort, filter_match_service: FilterMatchService):
        self.filter_match_port = filter_match_port
        self.filter_match_service = filter_match_service

    async def preprocess_all_job_offers(self, job_offer_ids: List[int]) -> List[dict]:
        ia_results = await self.filter_match_port.preprocess_all_job_offers(job_offer_ids)
        if not ia_results:
            return []
        response_list = []
        for res in ia_results:
            job_offer_id = res.get("job_offer_id") or res.get("id")
            await self.filter_match_service.save_filtered_job_offer(job_offer_id, res)
            embedding = res.get("embedding")
            if embedding is not None:
                job_offer = await self.filter_match_service.job_offer_repo.find_by_id(job_offer_id)
                if job_offer:
                    job_offer.embedding = embedding
                    await self.filter_match_service.job_offer_repo.update(job_offer)
            response_item = {
                "id": res.get("id", job_offer_id),
                "job_offer_id": job_offer_id,
                "student_id": None,
                "status": res.get("status", "processed"),
                "stage": res.get("stage", 1),
                "created_at": res.get("created_at"),
                "updated_at": res.get("updated_at"),
            }
            response_list.append(response_item)
        return response_list

    async def preprocess_job_offer(self, job_offer_id: int) -> dict:
        res = await self.filter_match_port.preprocess_job_offer(job_offer_id)
        if not res:
            raise ValueError("Error en el preprocesamiento de la oferta de trabajo")
        await self.filter_match_service.save_filtered_job_offer(job_offer_id, res)
        embedding = res.get("embedding")
        if embedding is not None:
            job_offer = await self.filter_match_service.job_offer_repo.find_by_id(job_offer_id)
            if job_offer:
                job_offer.embedding = embedding
                await self.filter_match_service.job_offer_repo.update(job_offer)
        response_item = {
            "id": res.get("id", job_offer_id),
            "job_offer_id": job_offer_id,
            "student_id": None,
            "status": res.get("status", "processed"),
            "stage": res.get("stage", 1),
            "created_at": res.get("created_at"),
            "updated_at": res.get("updated_at"),
        }
        return response_item

    async def preprocess_all_students(self, student_ids: List[int]) -> List[dict]:
        ia_results = await self.filter_match_port.preprocess_all_students(student_ids)
        if not ia_results:
            return []
        response_list = []
        for res in ia_results:
            student_id = res.get("student_id") or res.get("id")
            await self.filter_match_service.save_filtered_student(student_id, res)
            embedding = res.get("embedding")
            if embedding is not None:
                student = await self.filter_match_service.student_repo.find_by_id(student_id)
                if student:
                    student.embedding = embedding
                    await self.filter_match_service.student_repo.update(student)
            response_item = {
                "id": res.get("id", student_id),
                "job_offer_id": None,
                "student_id": student_id,
                "status": res.get("status", "processed"),
                "stage": res.get("stage", 1),
                "created_at": res.get("created_at"),
                "updated_at": res.get("updated_at"),
            }
            response_list.append(response_item)
        return response_list

    async def preprocess_student(self, student_id: int) -> dict:
        res = await self.filter_match_port.preprocess_student(student_id)
        if not res:
            raise ValueError("Error en el preprocesamiento del estudiante")
        await self.filter_match_service.save_filtered_student(student_id, res)
        embedding = res.get("embedding")
        if embedding is not None:
            student = await self.filter_match_service.student_repo.find_by_id(student_id)
            if student:
                student.embedding = embedding
                await self.filter_match_service.student_repo.update(student)
        response_item = {
            "id": res.get("id", student_id),
            "job_offer_id": None,
            "student_id": student_id,
            "status": res.get("status", "processed"),
            "stage": res.get("stage", 1),
            "created_at": res.get("created_at"),
            "updated_at": res.get("updated_at"),
        }
        return response_item

    async def register_filter_match_student(self, student_id: int, filter_match_data: dict) -> FilterMatch:
        if not filter_match_data:
            raise ValueError("No se recibieron datos de filtrado para registrar")
        filter_match_entity = self.filter_match_service.filter_match_entity(filter_match_data, student_id=student_id)
        saved_entity = await self.filter_match_port.register_filter_match_student(student_id, filter_match_entity)
        if not saved_entity:
            raise ValueError("Error al registrar el filtrado del estudiante")
        return saved_entity

    async def register_filter_match_job_offer(self, job_offer_id: int, filter_match_data: dict) -> FilterMatch:
        if not filter_match_data:
            raise ValueError("No se recibieron datos de filtrado para registrar")
        filter_match_entity = self.filter_match_service.filter_match_entity(filter_match_data, job_offer_id=job_offer_id)
        saved_entity = await self.filter_match_port.register_filter_match_job_offer(job_offer_id, filter_match_entity)
        if not saved_entity:
            raise ValueError("Error al registrar el filtrado de la oferta de trabajo")
        return saved_entity
