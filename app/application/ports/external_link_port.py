from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

from app.domain.entities.external_link import ExternalLink

class ExternalLinkPort(ABC):
    @abstractmethod
    async def register_external_link(self, external_link_data: Dict[str, Any]) -> ExternalLink:
        pass

    @abstractmethod
    async def get_external_link(self, external_link_id: int) -> Optional[ExternalLink]:
        pass

    @abstractmethod
    async def get_external_links_by_student_id(self, student_id: int) -> Optional[ExternalLink]:
        pass

    @abstractmethod
    async def get_all_external_links(self) -> List[ExternalLink]:
        pass

    @abstractmethod
    async def update_external_link(self, external_link_id: int, external_link_data: Dict[str, Any]) -> Optional[ExternalLink]:
        pass

    @abstractmethod
    async def delete_external_link(self, external_link_id: int) -> bool:
        pass