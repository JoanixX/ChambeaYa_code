from typing import Dict, Any, Optional
from datetime import datetime

from app.domain.entities.external_link import ExternalLink
from app.domain.repositories.external_link_repository import ExternalLinkRepository

class ExternalLinkService:
    def __init__(self, external_link_repo: ExternalLinkRepository):
        self.external_link_repo = external_link_repo

    async def register_external_link(self, external_link_data: Dict[str, Any]) -> int:
        external_link = self.external_link_entity(external_link_data)

        saved_model = await self.external_link_repo.save(external_link)
        if saved_model:
            return saved_model.id
        else:
            raise ValueError("Error al guardar el link")

    async def get_external_link(self, external_link_id: int) -> Optional[ExternalLink]:
        return await self.external_link_repo.find_by_id(external_link_id)

    async def get_all_external_links(self) -> list[ExternalLink]:
        return await self.external_link_repo.get_all()

    async def update_external_link(self, external_link_id: int, external_link_data: Dict[str, Any]) -> Optional[ExternalLink]:
        existing_external_link = await self.external_link_repo.find_by_id(external_link_id)
        if not existing_external_link:
            return None

        updated_external_link = ExternalLink(
            id=external_link_id,
            student_id=external_link_data.get("student_id", existing_external_link.student_id),
            link=external_link_data.get("link", existing_external_link.link)
        )

        await self.external_link_repo.update(updated_external_link)
        return updated_external_link

    async def delete_external_link(self, external_link_id: int) -> bool:
        return await self.external_link_repo.delete(external_link_id)

    def external_link_entity(self, external_link_data: Dict[str, Any]) -> ExternalLink:
        if 'created_at' not in external_link_data:
            external_link_data['created_at'] = datetime.now()
        if 'updated_at' not in external_link_data:
            external_link_data['updated_at'] = datetime.now()
        return ExternalLink(
            id=0,
            student_id=external_link_data.get("student_id", None),
            link=external_link_data.get("link", None),
            created_at=external_link_data['created_at'],
            updated_at=external_link_data['updated_at']
         )