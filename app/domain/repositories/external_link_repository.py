from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.external_link import ExternalLink

class ExternalLinkRepository(ABC):
    @abstractmethod
    async def save(self, external_link: ExternalLink):
        pass

    @abstractmethod
    async def find_by_id(self, external_link_id: int) -> Optional[ExternalLink]:
        pass

    @abstractmethod
    async def find_by_student_id(self, student_id: int) -> Optional[ExternalLink]:
        pass

    @abstractmethod
    async def get_all(self) -> list[ExternalLink]:
        pass

    @abstractmethod
    async def update(self, external_link: ExternalLink):
        pass

    @abstractmethod
    async def delete(self, external_link_id: int):
        pass