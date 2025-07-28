from app.domain.entities.skill import Skill
from app.domain.repositories.skill_repository import SkillRepository
from app.application.ports.skill_port import SkillPort

class AddSkillService:
    def __init__(self, skill_repo: SkillRepository, add_skill_port: SkillPort):
        self.skill_repo = skill_repo
        self.add_skill_port = add_skill_port
        
    async def add_skill(self, skill_data: dict):
        #validaciones de negocio básicas
        if await self.skill_repo.find_by_name(skill_data["name"]):
            raise ValueError("La habilidad ya está registrada")
        
        skill = Skill(
            id=0,  #se asigna automáticamente por la base de datos
            name=skill_data["name"],
        )

        #guardar habilidad usando el repositorio directamente
        skill_saved = await self.skill_repo.save(skill)
        if skill_saved:
            return skill_saved.id
        else:
            raise ValueError("Error al guardar la habilidad")