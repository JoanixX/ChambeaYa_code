from typing import Dict, Any, Optional
from datetime import datetime, date

from app.domain.entities.app_user import AppUser, UserRole
from app.domain.repositories.app_user_repository import AppUserRepository

class AppUserService:
    def __init__(self, user_repo: AppUserRepository):
        self.user_repo = user_repo

    async def get_by_email(self, email: str) -> Optional[AppUser]:
        return await self.user_repo.find_by_email(email)
    
    async def register_user(self, user_data: Dict[str, Any]) -> int:
        user = self.app_user_entity(user_data)
        saved_model = await self.user_repo.save(user)
        if saved_model:
            return saved_model.id
        else:
            raise ValueError("Error al guardar el usuario")

    async def authenticate(self, email: str, password: str, session) -> Optional[AppUser]:
        user = await self.user_repo.find_by_email(email)
        if not user:
            return None
        from app.core.security.jwt_utils import verify_password
        if not verify_password(password, user.password_hash):
            return None
        return user

    def app_user_entity(self, user_data: Dict[str, Any]) -> AppUser:
        if 'created_at' not in user_data:
            user_data['created_at'] = datetime.now()
        if 'updated_at' not in user_data:
            user_data['updated_at'] = datetime.now()

        role = user_data.get('role', 'student')
        if isinstance(role, str):
            role = UserRole(role)

        date_of_birth = user_data.get("date_of_birth")
        if date_of_birth:
            if isinstance(date_of_birth, str):
                try:
                    date_of_birth = date.fromisoformat(date_of_birth)
                except Exception:
                    date_of_birth = None
        else:
            date_of_birth = None

        email = user_data.get("email")
        dni = user_data.get("dni")
        name = user_data.get("name")
        location = user_data.get("location")
        password_hash = user_data.get("password_hash")
        related_id = user_data.get("related_id")
        cv_url = user_data.get("cv_url") if role == UserRole.student else None
        main_motivation = user_data.get("main_motivation") if role == UserRole.student else None
        description = user_data.get("description") if role == UserRole.student else None
        ruc = user_data.get("ruc") if role == UserRole.company else None

        return AppUser(
            id=0,
            email=email,
            dni=dni,
            cv_url=cv_url,
            name=name,
            location=location,
            ruc=ruc,
            date_of_birth=date_of_birth,
            main_motivation=main_motivation,
            description=description,
            password_hash=password_hash,
            role=role,
            related_id=related_id,
            created_at=user_data['created_at'],
            updated_at=user_data['updated_at']
        )