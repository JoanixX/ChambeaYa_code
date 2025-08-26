from abc import ABC, abstractmethod
from app.domain.entities.chat_history import ChatHistory
from typing import Optional

class ChatHistoryRepository(ABC):
    @abstractmethod
    async def save(self, chat_history: ChatHistory):
        pass

    @abstractmethod
    async def find_by_phone(self, chat_history_phone_number: str) -> Optional[ChatHistory]:
        pass

    @abstractmethod
    async def update(self, chat_history: ChatHistory):
        pass

    @abstractmethod
    async def delete(self, chat_history_phone_number: str):
        pass
