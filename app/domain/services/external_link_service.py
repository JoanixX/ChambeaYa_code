from app.domain.entities.external_link import ExternalLink
from app.domain.repositories.external_link_repository import ExternalLinkRepository
from datetime import datetime
from typing import Dict, Any, Optional

class ExternalLinkService:
    def __init__(self, external_link_repo: ExternalLinkRepository):
        self.external_link_repo = external_link_repo

    async def register_external_link(self, link_data: Dict[str, Any]) -> int:
        link = ExternalLink(
            id=0,
            url=link_data["url"],
            description=link_data.get("description", ""),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        saved_model = await self.external_link_repo.save(link)
        if saved_model:
            return saved_model.id
        else:
            raise ValueError("Error al guardar el enlace externo")
    
    async def get_external_link(self, link_id: int) -> Optional[ExternalLink]:
        return await self.external_link_repo.find_by_id(link_id)
    
    async def get_all_external_links(self) -> list[ExternalLink]:
        return await self.external_link_repo.get_all()

    async def delete_external_link(self, link_id: int) -> bool:
        return await self.external_link_repo.delete(link_id)
    
    async def get_name_by_id(self, link_id: int) -> Optional[str]:
        return await self.external_link_repo.get_name_by_id(link_id)