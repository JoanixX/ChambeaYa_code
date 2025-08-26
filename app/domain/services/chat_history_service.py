from typing import Dict, Any, Optional
from datetime import datetime

from app.domain.entities.chat_history import ChatHistory
from app.domain.repositories.chat_history_repository import ChatHistoryRepository

class ChatHistoryService:
    def __init__(self, chat_history_repo: ChatHistoryRepository):
        self.chat_history_repo = chat_history_repo

    async def register_chat_history(self, chat_history_data: Dict[str, Any]) -> int:
        chat_history = self.chat_history_entity(chat_history_data)

        saved_model = await self.chat_history_repo.save(chat_history)
        if saved_model:
            return saved_model.id
        else:
            raise ValueError("Error al guardar el historial")

    async def get_chat_history(self, chat_history_id: int) -> Optional[ChatHistory]:
        return await self.chat_history_repo.find_by_phone(chat_history_id)

    async def update_chat_history(self, chat_history_phone_number: str, chat_history_data: Dict[str, Any]) -> Optional[ChatHistory]:
        existing_chat_history = await self.chat_history_repo.find_by_phone(chat_history_phone_number)
        if not existing_chat_history:
            return None

        updated_chat_history = ChatHistory(
            id=chat_history_data.get("id", existing_chat_history.id),
            phone_number=chat_history_phone_number,
            message_order=chat_history_data.get("message_order", existing_chat_history.message_order),
            message_role=chat_history_data.get("message_role", existing_chat_history.message_role),
            message=chat_history_data.get("message", existing_chat_history.message)
        )

        await self.chat_history_repo.update(updated_chat_history)
        return updated_chat_history

    async def delete_chat_history(self, chat_history_id: int) -> bool:
        return await self.chat_history_repo.delete(chat_history_id)
    
    def chat_history_entity(self, chat_history_data: Dict[str, Any]) -> ChatHistory:
        if 'created_at' not in chat_history_data:
            chat_history_data['created_at'] = datetime.now()
        if 'updated_at' not in chat_history_data:
            chat_history_data['updated_at'] = datetime.now()
        return ChatHistory(
            id=0,  # se asignará automáticamente por la base de datos
            phone_number=chat_history_data.get("phone_number", None),
            message_order=chat_history_data.get("message_order", None),
            message_role=chat_history_data.get("message_role", None),
            message=chat_history_data.get("message", None),
            created_at=chat_history_data.get("created_at"),
            updated_at=chat_history_data.get("updated_at")
        )