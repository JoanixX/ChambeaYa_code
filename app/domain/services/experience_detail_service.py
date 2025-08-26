from typing import Dict, Any, Optional
from datetime import datetime

from app.domain.entities.experience_detail import ExperienceDetail
from app.domain.repositories.experience_detail_repository import ExperienceDetailRepository

class ExperienceDetailService:
    def __init__(self, experience_detail_repo: ExperienceDetailRepository):
        self.experience_detail_repo = experience_detail_repo

    async def register_experience_detail(self, experience_detail_data: Dict[str, Any]) -> int:
        experience_detail = self.experience_detail_entity(experience_detail_data)

        saved_model = await self.experience_detail_repo.save(experience_detail)
        if saved_model:
            return saved_model.id
        else:
            raise ValueError("Error al guardar la experiencia")

    async def get_experience_detail(self, experience_detail_id: int) -> Optional[ExperienceDetail]:
        return await self.experience_detail_repo.find_by_id(experience_detail_id)

    async def get_all_experience_details(self) -> list[ExperienceDetail]:
        return await self.experience_detail_repo.get_all()

    async def update_experience_detail(self, experience_detail_id: int, experience_detail_data: Dict[str, Any]) -> Optional[ExperienceDetail]:
        existing_experience_detail = await self.experience_detail_repo.find_by_id(experience_detail_id)
        if not existing_experience_detail:
            return None

        updated_experience_detail = ExperienceDetail(
            id=experience_detail_id,
            student_id=experience_detail_data.get("student_id", existing_experience_detail.student_id),
            job_offer_id=experience_detail_data.get("job_offer_id", existing_experience_detail.job_offer_id),
            name=experience_detail_data.get("name", existing_experience_detail.name),
            description=experience_detail_data.get("description", existing_experience_detail.description),
            duration_in_months=experience_detail_data.get("duration_in_months", existing_experience_detail.duration_in_months)
        )

        await self.experience_detail_repo.update(updated_experience_detail)
        return updated_experience_detail

    async def delete_experience_detail(self, experience_detail_id: int) -> bool:
        return await self.experience_detail_repo.delete(experience_detail_id)

    def experience_detail_entity(self, experience_detail_data: Dict[str, Any]) -> ExperienceDetail:
        if 'created_at' not in experience_detail_data:
            experience_detail_data['created_at'] = datetime.now()
        if 'updated_at' not in experience_detail_data:
            experience_detail_data['updated_at'] = datetime.now()
        return ExperienceDetail(
            id=0,
            student_id=experience_detail_data.get("student_id", None),
            job_offer_id=experience_detail_data.get("job_offer_id", None),
            name=experience_detail_data.get("name", None),
            description=experience_detail_data.get("description", None),
            duration_in_months=experience_detail_data.get("duration_in_months", None),
            created_at=experience_detail_data['created_at'],
            updated_at=experience_detail_data['updated_at']
         )