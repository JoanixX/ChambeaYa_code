from typing import List
from app.domain.entities.job_offer_required_skill import JobOfferRequiredSkill
from app.domain.services.job_offer_required_skill_service import JobOfferRequiredSkillService
from app.application.ports.job_offer_required_skill_port import JobOfferRequiredSkillPort

class JobOfferRequiredSkillUseCase:
    def __init__(self, job_offer_required_skill_port: JobOfferRequiredSkillPort, 
                 job_offer_required_skill_service: JobOfferRequiredSkillService):
        self.job_offer_required_skill_port = job_offer_required_skill_port
        self.job_offer_required_skill_service = job_offer_required_skill_service

    async def get_job_offer_required_skills(self, job_offer_id: int) -> List[JobOfferRequiredSkill]:
        return await self.job_offer_required_skill_service.get_job_offer_required_skills(job_offer_id)

    async def add_job_offer_required_skill(self, job_offer_required_skill: JobOfferRequiredSkill) -> JobOfferRequiredSkill:
        job_offer_required_skill_id = await self.job_offer_required_skill_port.add_job_offer_required_skill(job_offer_required_skill)

        if not job_offer_required_skill_id:
            raise ValueError("Error al agregar la habilidad al estudiante")

        return job_offer_required_skill_id

    async def delete_job_offer_required_skill(self, job_offer_id: int, skill_id: int) -> None:
        success = await self.job_offer_required_skill_port.delete_job_offer_required_skill(job_offer_id, skill_id)

        if not success:
            raise ValueError(f"Error al eliminar la habilidad con ID {skill_id} de la oferta de trabajo con ID {job_offer_id}")

        return {
            "message": "Habilidad eliminada exitosamente de la oferta de trabajo"
        }