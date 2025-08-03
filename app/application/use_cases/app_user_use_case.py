from app.domain.entities.app_user import AppUser, UserRole
from app.domain.services.app_user_service import AppUserService
from app.domain.repositories.app_user_repository import AppUserRepository
from app.core.security.jwt_utils import get_password_hash

class AppUserUseCase:
    def __init__(self, repository: AppUserRepository, service: AppUserService):
        self.repository = repository
        self.service = service

    async def register_user(self, email: str, password: str, role: UserRole, related_id: int) -> AppUser:
        if await self.service.is_email_taken(email):
            raise ValueError("El usuario ya existe")

        password_hash = get_password_hash(password)

        user = AppUser(
            id=0,
            email=email,
            password_hash=password_hash,
            role=role,
            related_id=related_id
        )

        return await self.repository.save(user)