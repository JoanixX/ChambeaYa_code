from typing import Optional, List, Dict, Any

from app.domain.entities.interest import Interest
from app.application.ports.interest_port import InterestPort
from app.domain.services.interest_service import InterestService
from app.adapters.input.fastapi.schemas.interest_schema import InterestResponse

class InterestUseCase:
    def __init__(self, interest_port: InterestPort, interest_service: InterestService):
        self.interest_port = interest_port
        self.interest_service = interest_service

    async def register_interest(self, interest_data: Dict[str, Any]) -> int:
        interest_id = await self.interest_service.register_interest(interest_data)

        if not interest_id:
            raise ValueError("Error al guardar el interés")

        return interest_id

    async def get_all_interests(self) -> List[Interest]:
        interests = await self.interest_port.get_all_interests()
        return [InterestResponse(id=s.id, name=s.name) for s in interests]
    
    async def get_interest(self, interest_id: int) -> Interest:
        interest = await self.interest_port.get_interest(interest_id)
        if not interest:
            raise ValueError(f"Interés con ID {interest_id} no encontrado")
        return InterestResponse(id=interest.id, name=interest.name)
    
    async def delete_interest(self, interest_id: int) -> dict:
        interest = await self.interest_port.get_interest(interest_id)
        if not interest:
            raise ValueError(f"Interés con ID {interest_id} no encontrado")

        success = await self.interest_port.delete_interest(interest_id)
        if not success:
            raise ValueError(f"Error al eliminar interés con ID {interest_id}")

        return {
            "message": "Interés eliminado exitosamente"
        }
    
    async def get_interest_name_by_id(self, interest_id: int) -> Optional[str]:
        interest_name = await self.interest_port.get_interest_name_by_id(interest_id)
        if not interest_name:
            raise ValueError(f"Interés con ID {interest_id} no encontrado")
        return interest_name