from sqlalchemy.future import select
from sqlalchemy import delete
from typing import Optional

from app.domain.repositories.chat_history_repository import ChatHistoryRepository
from app.domain.entities.chat_history import ChatHistory
from app.adapters.output.orm.models.chat_history_model import ChatHistoryModel

class ChatHistoryRepositoryImpl(ChatHistoryRepository):
    def __init__(self, session):
        self.session = session

    async def save(self, chat_history: ChatHistory):
        model = ChatHistoryModel(
            phone_number=chat_history.phone_number,
            message_order=chat_history.message_order,
            message_role=chat_history.message_role,
            message=chat_history.message
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def find_by_phone(self, chat_history_phone_number: str) -> Optional[ChatHistory]:
        result = await self.session.execute(select(ChatHistoryModel).where(ChatHistoryModel.phone_number == chat_history_phone_number))
        model = result.scalar_one_or_none()
        if model:
            return ChatHistory(
                id=model.id,
                phone_number=model.phone_number,
                message_order=model.message_order,
                message_role=model.message_role,
                message=model.message,
                created_at=model.created_at,
                updated_at=model.updated_at
            )
        return None

    async def update(self, chat_history: ChatHistory) -> Optional[ChatHistory]:
        result = await self.session.execute(select(ChatHistoryModel).where(ChatHistoryModel.phone_number == chat_history.phone_number))
        model = result.scalar_one_or_none()
        if model:
            model.message_order = chat_history.message_order
            model.message_role = chat_history.message_role
            model.message = chat_history.message
            await self.session.commit()
            await self.session.refresh(model)
            return chat_history
        return None

    async def delete(self, chat_history_phone_number: str):
        result = await self.session.execute(select(ChatHistoryModel).where(ChatHistoryModel.phone_number == chat_history_phone_number))
        model = result.scalar_one_or_none()
        if not model:
            return False

        await self.session.execute(delete(ChatHistoryModel).where(ChatHistoryModel.phone_number == chat_history_phone_number))
        await self.session.commit()
        return True
