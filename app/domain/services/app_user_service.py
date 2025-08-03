from app.domain.repositories.app_user_repository import AppUserRepository

class AppUserService:
    def __init__(self, repository: AppUserRepository):
        self.repository = repository

    async def is_email_taken(self, email: str) -> bool:
        user = await self.repository.find_by_email(email)
        return user is not None
