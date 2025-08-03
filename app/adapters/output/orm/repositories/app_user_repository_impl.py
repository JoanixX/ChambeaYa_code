from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.adapters.output.orm.models.app_user_model import AppUserModel
from app.domain.entities.app_user import AppUser, UserRole
from app.domain.repositories.app_user_repository import AppUserRepository

class AppUserRepositoryImpl(AppUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_by_email(self, email: str) -> AppUser | None:
        result = await self.session.execute(select(AppUserModel).where(AppUserModel.email == email))
        row = result.scalar_one_or_none()
        if row:
            return AppUser(
                id=row.id,
                email=row.email,
                password_hash=row.password_hash,
                role=UserRole(row.role),
                related_id=row.related_id
            )
        return None

    async def save(self, user: AppUser) -> AppUser:
        model = AppUserModel(
            email=user.email,
            password_hash=user.password_hash,
            role=user.role.value,
            related_id=user.related_id
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return AppUser(
            id=model.id,
            email=model.email,
            password_hash=model.password_hash,
            role=UserRole(model.role),
            related_id=model.related_id
        )