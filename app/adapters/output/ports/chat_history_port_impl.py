from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from datetime import datetime

from app.adapters.output.orm.repositories.chat_history_repository_impl import ChatHistoryRepositoryImpl
from app.application.ports.chat_history_port import ChatHistoryPort
from app.domain.entities.chat_history import ChatHistory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatHistoryPortImpl(ChatHistoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.chat_history_repo = ChatHistoryRepositoryImpl(session)

    async def register_chat_history(self, message_data: Dict[str, Any]) -> int:
        if 'created_at' not in message_data:
            message_data['created_at'] = datetime.now()
        if 'updated_at' not in message_data:
            message_data['updated_at'] = datetime.now()
        chat_history = ChatHistory(
            id=0,
            phone_number=message_data['phone_number'],
            message_order=message_data['message_order'],
            message_role=message_data['message_role'],
            message=message_data['message'],
            created_at=message_data['created_at'],
            updated_at=message_data['updated_at']
        )

        saved_chat_history = await self.chat_history_repo.save(chat_history)
        return saved_chat_history.id
    
    async def get_chat_history(self, chat_history_phone_number: str) -> Optional[ChatHistory]:
        return await self.chat_history_repo.find_by_phone(chat_history_phone_number)
    
    async def delete_chat_history(self, chat_history_phone_number: str) -> bool:
        return await self.chat_history_repo.delete(chat_history_phone_number)
    
    async def validate_chat_history_data(self, chat_history_data: Dict[str, Any]) -> bool:
        logger.info("Validando datos del historial de chat_ {chat_history_data}")
        
        required_fields = ['phone_number', 'message_order', 'message_role', 'message']

        for field in required_fields:
            if field not in chat_history_data:
                logger.error(f"Campo requerido '{field}' está vacío o no existe.")
                return False
        
        logger.info("Datos de la empresa validados correctamente.")
        return True