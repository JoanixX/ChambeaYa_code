from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.app_user_use_case import AppUserUseCase
from app.adapters.output.orm.repositories.app_user_repository_impl import AppUserRepositoryImpl
from app.domain.services.app_user_service import AppUserService
from app.adapters.output.ports.app_user_port_impl import AppUserPortImpl

class AppUserUseCaseFactory:
    def __init__(self, session: AsyncSession):
        self.session = session

    def build(self) -> AppUserUseCase:
        app_user_port = AppUserPortImpl(self.session)
        app_user_repo = AppUserRepositoryImpl(self.session)
        app_user_service = AppUserService(app_user_repo)
        return AppUserUseCase(app_user_port, app_user_service)