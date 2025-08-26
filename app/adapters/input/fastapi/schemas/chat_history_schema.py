from pydantic import BaseModel, Field, field_validator
from app.adapters.input.fastapi.validators import not_empty

class ChatHistoryCreate(BaseModel):
    phone_number: str = Field(..., description="Número de teléfono del usuario")
    message_order: int = Field(..., description="Orden del mensaje en la conversación")
    message_role: str = Field(..., description="Rol del mensaje (user, assistant")
    message: str = Field(..., description="Contenido del mensaje")

    @field_validator('phone_number', 'message_role', 'message')
    def not_empty_fields(cls, v, info):
        return not_empty(v, info.field_name)
    
class ChatHistoryResponse(BaseModel):
    id: int
    phone_number: str
    message_order: int
    message_role: str
    message: str