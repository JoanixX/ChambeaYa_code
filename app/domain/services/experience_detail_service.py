from app.domain.entities.experience_detail import ExperienceDetail
from app.domain.repositories.experience_detail_repository import ExperienceDetailRepository
from typing import Dict, Any, Optional

class ExperienceDetailService:
    def __init__(self, experience_detail_repo: ExperienceDetailRepository):
        self.experience_detail_repo = experience_detail_repo

    async def register_experience_detail(self, experience_detail_data: Dict[str, Any]) -> int:
        experience_detail = ExperienceDetail(
            id=0,
            name=experience_detail_data["name"],
            description=experience_detail_data.get("description", ""),
            duration_in_months= experience_detail_data.get("duration_in_months", 0),
        )
        saved_model = await self.experience_detail_repo.save(experience_detail)
        if saved_model:
            return saved_model.id
        else:
            raise ValueError("Error al guardar el detalle de la experiencia")
        
    async def get_experience_detail(self, experience_id: int) -> Optional[ExperienceDetail]:
        return await self.experience_detail_repo.find_by_id(experience_id)
    
    async def get_all_experience_details(self) -> list[ExperienceDetail]:
        return await self.experience_detail_repo.get_all()

    async def delete_experience_detail(self, experience_id: int) -> bool:
        return await self.experience_detail_repo.delete(experience_id)
    
    async def get_name_by_id(self, experience_id: int) -> Optional[str]:
        return await self.experience_detail_repo.get_name_by_id(experience_id)