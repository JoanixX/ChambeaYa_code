from abc import ABC, abstractmethod
from app.domain.entities.app_user import AppUser

class AppUserRepository(ABC):
    @abstractmethod
    async def find_by_email(self, email: str) -> AppUser | None:
        pass
    
    @abstractmethod
    async def save(self, user: AppUser) -> AppUser:
        pass
