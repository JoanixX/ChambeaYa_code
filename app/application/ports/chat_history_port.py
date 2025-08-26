from abc import ABC, abstractmethod
from app.domain.entities.chat_history import ChatHistory
from typing import Optional, Dict, Any, List

class ChatHistoryPort(ABC):
    @abstractmethod
    async def register_chat_history(self, message_data: Dict[str, Any]) -> int:
        pass

    @abstractmethod
    async def get_chat_history(self, chat_history_phone_number: str) -> Optional[ChatHistory]:
        pass

    @abstractmethod
    async def delete_chat_history(self, chat_history_phone_number: str) -> bool:
        pass

    @abstractmethod
    async def validate_chat_history_data(self, chat_history_data: Dict[str, Any]) -> bool:
        pass