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
            role_value = row.role.value if isinstance(row.role, UserRole) else row.role
            return AppUser(
                id=row.id,
                email=row.email,
                dni=row.dni,
                cv_url=row.cv_url,
                name=row.name,
                location=row.location,
                ruc=row.ruc,
                date_of_birth=row.date_of_birth,
                main_motivation=row.main_motivation,
                description=row.description,
                password_hash=row.password_hash,
                role=role_value,
                related_id=row.related_id,
                created_at=row.created_at,
                updated_at=row.updated_at,
                deleted_at=row.deleted_at
            )
        return None

    async def save(self, user: AppUser) -> AppUser:
        model = AppUserModel(
            email=user.email,
            dni=user.dni,
            cv_url=user.cv_url,
            name=user.name,
            location=user.location,
            ruc=user.ruc,
            date_of_birth=user.date_of_birth,
            main_motivation=user.main_motivation,
            description=user.description,
            password_hash=user.password_hash,
            role=user.role.value if isinstance(user.role, UserRole) else user.role,
            related_id=user.related_id
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        role_value = model.role.value if isinstance(model.role, UserRole) else model.role
        return AppUser(
            id=model.id,
            email=model.email,
            dni=model.dni,
            cv_url=model.cv_url,
            name=model.name,
            location=model.location,
            ruc=model.ruc,
            date_of_birth=model.date_of_birth,
            main_motivation=model.main_motivation,
            description=model.description,
            password_hash=model.password_hash,
            role=role_value,
            related_id=model.related_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at
        )