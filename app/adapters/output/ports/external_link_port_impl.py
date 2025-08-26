from typing import Dict, Any, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from datetime import datetime

from app.adapters.output.orm.repositories.external_link_repository_impl import ExternalLinkRepositoryImpl
from app.application.ports.external_link_port import ExternalLinkPort
from app.domain.entities.external_link import ExternalLink

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExternalLinkPortImpl(ExternalLinkPort):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.external_link_repo = ExternalLinkRepositoryImpl(session)

    async def register_external_link(self, external_link_data: Dict[str, Any]) -> ExternalLink:
        if 'created_at' not in external_link_data:
            external_link_data['created_at'] = datetime.now()
        if 'updated_at' not in external_link_data:
            external_link_data['updated_at'] = datetime.now()
        external_link = ExternalLink(
            id=0,
            student_id=external_link_data["student_id"],
            link=external_link_data["link"],
            created_at=external_link_data['created_at'],
            updated_at=external_link_data['updated_at']
        )
        saved_external_link = await self.external_link_repo.save(external_link)
        return saved_external_link

    async def get_external_link(self, external_link_id: int) -> Optional[ExternalLink]:
        return await self.external_link_repo.find_by_id(external_link_id)
    
    async def get_external_links_by_student_id(self, student_id: int) -> Optional[ExternalLink]:
        return await self.external_link_repo.find_by_student_id(student_id)

    async def get_all_external_links(self) -> List[ExternalLink]:
        return await self.external_link_repo.get_all()

    async def update_external_link(self, external_link_id: int, external_link_data: Dict[str, Any]) -> Optional[ExternalLink]:
        existing_external_link = await self.external_link_repo.find_by_id(external_link_id)
        if not existing_external_link:
            return None
        if 'created_at' not in external_link_data:
            external_link_data['created_at'] = existing_external_link.created_at
        if 'updated_at' not in external_link_data:
            external_link_data['updated_at'] = datetime.now()
        updated_external_link = ExternalLink(
            id=external_link_id,
            student_id=external_link_data.get("student_id", existing_external_link.student_id),
            link=external_link_data.get("link", existing_external_link.link),
            created_at=external_link_data['created_at'],
            updated_at=external_link_data['updated_at'],
        )
        return await self.external_link_repo.update(updated_external_link)

    async def delete_external_link(self, external_link_id: int) -> bool:
        return await self.external_link_repo.delete(external_link_id)