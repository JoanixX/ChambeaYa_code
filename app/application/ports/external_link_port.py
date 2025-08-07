from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List

from app.domain.entities.external_link import ExternalLink

class ExternalLinkPort(ABC):
    @abstractmethod
    async def register_external_link(self, link_data: Dict[str, Any]) -> ExternalLink:
        pass

    @abstractmethod
    async def get_external_link(self, link_id: int) -> Optional[ExternalLink]:
        pass

    @abstractmethod
    async def get_all_external_links(self) -> List[ExternalLink]:
        pass

    @abstractmethod
    async def delete_external_link(self, link_id: int) -> bool:
        pass

    @abstractmethod
    async def get_external_link_url_by_id(self, link_id: int) -> Optional[str]:
        pass