from app.domain.entities.interest import Interest
from app.domain.repositories.interest_repository import InterestRepository
from typing import Dict, Any, Optional

class InterestService:
    def __init__(self, interest_repo: InterestRepository):
        self.interest_repo = interest_repo

    async def register_interest(self, interest_data: Dict[str, Any]) -> int:
        interest = self.interest_entity(interest_data)

        saved_model = await self.interest_repo.save(interest)
        if saved_model:
            return saved_model.id
        else:
            raise ValueError("Error al guardar el interest")
        
    async def get_interest(self, interest_id: int) -> Optional[Interest]:
        return await self.interest_repo.find_by_id(interest_id)
    
    async def get_all_interests(self) -> list[Interest]:
        return await self.interest_repo.get_all()
    
    async def delete_interest(self, interest_id: int) -> bool:
        return await self.interest_repo.delete(interest_id)
    
    async def get_name_by_id(self, interest_data: int) -> Optional[str]:
        return await self.interest_repo.get_name_by_id(interest_data)

    def interest_entity(self, interest_data: Dict[str, Any]) -> Interest:
        return Interest(
            id=0,
            name=interest_data.get("name", None)
        )