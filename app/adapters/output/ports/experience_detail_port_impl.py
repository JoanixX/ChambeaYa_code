from typing import Dict, Any, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from datetime import datetime

from app.adapters.output.orm.repositories.experience_detail_repository_impl import ExperienceDetailRepositoryImpl
from app.application.ports.experience_detail_port import ExperienceDetailPort
from app.domain.entities.experience_detail import ExperienceDetail

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExperienceDetailPortImpl(ExperienceDetailPort):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.experience_detail_repo = ExperienceDetailRepositoryImpl(session)

    async def register_experience_detail(self, experience_detail_data: Dict[str, Any]) -> ExperienceDetail:
        if 'created_at' not in experience_detail_data:
            experience_detail_data['created_at'] = datetime.now()
        if 'updated_at' not in experience_detail_data:
            experience_detail_data['updated_at'] = datetime.now()
        experience_detail = ExperienceDetail(
            id=0,
            student_id=experience_detail_data["student_id"],
            job_offer_id=experience_detail_data["job_offer_id"],
            name=experience_detail_data["name"],
            description=experience_detail_data["description"],
            duration_in_months=experience_detail_data["duration_in_months"],
            created_at=experience_detail_data['created_at'],
            updated_at=experience_detail_data['updated_at'],
            deleted_at=experience_detail_data.get('deleted_at')
        )
        saved_experience_detail = await self.experience_detail_repo.save(experience_detail)
        return saved_experience_detail

    async def get_experience_detail(self, experience_detail_id: int) -> Optional[ExperienceDetail]:
        return await self.experience_detail_repo.find_by_id(experience_detail_id)

    async def get_experience_details_by_job_offer_id(self, job_offer_id: int) -> Optional[ExperienceDetail]:
        return await self.experience_detail_repo.find_by_job_offer_id(job_offer_id)

    async def get_experience_details_by_student_id(self, student_id: int) -> Optional[ExperienceDetail]:
        return await self.experience_detail_repo.find_by_student_id(student_id)

    async def get_all_experience_details(self) -> List[ExperienceDetail]:
        return await self.experience_detail_repo.get_all()

    async def update_experience_detail(self, experience_detail_id: int, experience_detail_data: Dict[str, Any]) -> Optional[ExperienceDetail]:
        existing_experience_detail = await self.experience_detail_repo.find_by_id(experience_detail_id)
        if not existing_experience_detail:
            return None
        if 'created_at' not in experience_detail_data:
            experience_detail_data['created_at'] = existing_experience_detail.created_at
        if 'updated_at' not in experience_detail_data:
            experience_detail_data['updated_at'] = datetime.now()
        updated_experience_detail = ExperienceDetail(
            id=experience_detail_id,
            student_id=experience_detail_data.get("student_id", existing_experience_detail.student_id),
            job_offer_id=experience_detail_data.get("job_offer_id", existing_experience_detail.job_offer_id),
            name=experience_detail_data.get("name", existing_experience_detail.name),
            description=experience_detail_data.get("description", existing_experience_detail.description),
            duration_in_months=experience_detail_data.get("duration_in_months", existing_experience_detail.duration_in_months),
            created_at=experience_detail_data['created_at'],
            updated_at=experience_detail_data['updated_at'],
            deleted_at=experience_detail_data.get('deleted_at', existing_experience_detail.deleted_at)
        )
        return await self.experience_detail_repo.update(updated_experience_detail)

    async def delete_experience_detail(self, experience_detail_id: int) -> bool:
        return await self.experience_detail_repo.delete(experience_detail_id)