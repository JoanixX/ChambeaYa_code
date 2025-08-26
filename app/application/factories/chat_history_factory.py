from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.chat_history_use_case import ChatHistoryUseCase
from app.adapters.output.orm.repositories.chat_history_repository_impl import ChatHistoryRepositoryImpl
from app.domain.services.chat_history_service import ChatHistoryService
from app.adapters.output.ports.chat_history_port_impl import ChatHistoryPortImpl

class ChatHistoryUseCaseFactory:
    def __init__(self, session: AsyncSession):
        self.session = session

    def build(self) -> ChatHistoryUseCase:
        chat_history_port = ChatHistoryPortImpl(self.session)
        chat_history_repo = ChatHistoryRepositoryImpl(self.session)
        chat_history_service = ChatHistoryService(chat_history_repo)
        return ChatHistoryUseCase(chat_history_port, chat_history_service)