from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.adapters.output.orm.models.app_user_model import AppUserModel
from app.domain.entities.app_user import AppUser, UserRole
from app.application.ports.app_user_port import AppUserPort

class AppUserPortImpl(AppUserPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> AppUser | None:
        result = await self.session.execute(select(AppUserModel).where(AppUserModel.email == email))
        user = result.scalar_one_or_none()
        if not user:
            return None
        return AppUser(id=user.id, email=user.email, password_hash=user.password_hash, role=UserRole(user.role), related_id=user.related_id)

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
        return AppUser(id=model.id, email=model.email, password_hash=model.password_hash, role=UserRole(model.role), related_id=model.related_id)
