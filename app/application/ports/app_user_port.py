from abc import ABC, abstractmethod
from app.domain.entities.app_user import AppUser

class AppUserPort(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> AppUser | None:
        pass
    
    @abstractmethod
    async def register_user(self, user: AppUser) -> AppUser:
        pass