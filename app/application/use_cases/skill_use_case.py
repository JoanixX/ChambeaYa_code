from app.application.ports.skill_port import SkillPort
from app.domain.services.skill_service import SkillService
from typing import Optional, List, Dict, Any

from app.adapters.input.fastapi.schemas.skill_schema import SkillResponse

class SkillUseCase:
    def __init__(self, skill_port: SkillPort, skill_service: SkillService):
        self.skill_port = skill_port
        self.skill_service = skill_service

    async def register_skill(self, skill_data: Dict[str, Any]) -> int:
        skill_id = await self.skill_service.register_skill(skill_data)

        if not skill_id:
            raise ValueError("Error al guardar el skill")

        return skill_id

    async def get_all_skills(self) -> List[SkillResponse]:
        skills = await self.skill_port.get_all_skills()
        return [SkillResponse(id=s.id, name=s.name) for s in skills]
    
    async def get_skill(self, skill_id: int) -> SkillResponse:
        skill = await self.skill_port.get_skill(skill_id)
        if not skill:
            raise ValueError(f"Skill con ID {skill_id} no encontrado")
        return SkillResponse(id=skill.id, name=skill.name)
    
    async def delete_skill(self, skill_id: int) -> Dict[str, Any]:
        skill = await self.skill_port.get_skill(skill_id)
        if not skill:
            raise ValueError(f"Skill con ID {skill_id} no encontrado")

        success = await self.skill_port.delete_skill(skill_id)
        if not success:
            raise ValueError(f"Error al eliminar skill con ID {skill_id}")

        return {
            "message": "Skill eliminado exitosamente"
        }
    
    async def get_skill_name_by_id(self, skill_id: int) -> Optional[str]:
        skill_name = await self.skill_port.get_skill_name_by_id(skill_id)
        if not skill_name:
            raise ValueError(f"Skill con ID {skill_id} no encontrado")
        return skill_name