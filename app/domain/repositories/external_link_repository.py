from abc import ABC, abstractmethod
from app.domain.entities.external_link import ExternalLink
from typing import Optional

class ExternalLinkRepository(ABC):
    @abstractmethod
    async def save(self, external_link: ExternalLink) -> ExternalLink:
        pass

    @abstractmethod
    async def find_by_id(self, linkexternal_link_id_id: int) -> Optional[ExternalLink]:
        pass

    @abstractmethod
    async def get_all(self) -> list[ExternalLink]:
        pass

    @abstractmethod
    async def update(self, external_link_id: int) -> Optional[ExternalLink]:
        pass

    @abstractmethod
    async def delete(self, external_link_id: int) -> bool:
        pass

    @abstractmethod
    async def get_name_by_id(self, link_id: int) -> Optional[str]:
        pass