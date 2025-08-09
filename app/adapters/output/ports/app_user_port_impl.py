from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict, Any
from datetime import datetime

from app.adapters.output.orm.repositories.app_user_repository_impl import AppUserRepositoryImpl
from app.domain.entities.app_user import AppUser, UserRole
from app.application.ports.app_user_port import AppUserPort

class AppUserPortImpl(AppUserPort):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.app_user_repo = AppUserRepositoryImpl(session)

    async def get_by_email(self, email: str) -> Optional[AppUser]:
        return await self.app_user_repo.find_by_email(email)

    async def register_user(self, user_data: Dict[str, Any]) -> AppUser:
        if 'created_at' not in user_data:
            user_data['created_at'] = datetime.now()
        if 'updated_at' not in user_data:
            user_data['updated_at'] = datetime.now()
        app_user = AppUser(
            id=0,
            email=user_data['email'],
            dni=user_data['dni'],
            cv_url=user_data.get('cv_url', ''),
            name=user_data.get('name', ''),
            location=user_data.get('location', ''),
            ruc=user_data.get('ruc', ''),
            date_of_birth=user_data.get('date_of_birth', None),
            password_hash=user_data['password_hash'],
            role=UserRole(user_data['role']),
            related_id=user_data['related_id'],
            created_at=user_data['created_at'],
            updated_at=user_data['updated_at'],
            deleted_at=user_data.get('deleted_at', None)
        )
        saved_app_user = await self.app_user_repo.save(app_user)
        return saved_app_user
