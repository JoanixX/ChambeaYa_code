from app.application.ports.chat_history_port import ChatHistoryPort
from app.domain.entities.chat_history import ChatHistory
from app.domain.services.chat_history_service import ChatHistoryService
from typing import Dict, Any, List

class ChatHistoryUseCase:
    def __init__(self, chat_history_port: ChatHistoryPort, chat_history_service: ChatHistoryService):
        self.chat_history_port = chat_history_port
        self.chat_history_service = chat_history_service

    async def register_chat_history(self, chat_history_data: Dict[str, Any]) -> Dict[str, Any]:
        if not await self.chat_history_port.validate_chat_history_data(chat_history_data):
            raise ValueError("Datos del mensaje inválidos")

        message_id = await self.chat_history_service.register_chat_history(chat_history_data)

        if not message_id:
            raise ValueError("Error al guardar el mensaje")

        return {
            "message_id": message_id,
            "registration_success": True,
            "message": "Historial registrado exitosamente"
        }
    
    async def get_chat_history(self, chat_history_phone_number: str) -> List[ChatHistory]:
        messages = await self.chat_history_port.get_chat_history(chat_history_phone_number)
        if messages is None:
            raise ValueError(f"No se encontraron mensajes para el número {chat_history_phone_number}")
        return messages
    
    async def delete_messages_by_phone(self, chat_history_phone_number: str) -> Dict[str, Any]:
        messages = await self.chat_history_port.get_chat_history(chat_history_phone_number)
        if messages is None:
            raise ValueError(f"No se encontraron mensajes para el número {chat_history_phone_number}")

        success = await self.chat_history_port.delete_chat_history(chat_history_phone_number)
        if not success:
            raise ValueError(f"Error al eliminar mensajes para el número {chat_history_phone_number}")

        return {
            "message": "Historial eliminado exitosamente"
        }