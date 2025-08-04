from typing import Dict, Any, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.output.orm.repositories.interest_repository_impl import InterestRepositoryImpl
from app.application.ports.interest_port import InterestPort
from app.domain.entities.interest import Interest

class InterestPortImpl(InterestPort):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.interest_repo = InterestRepositoryImpl(session)

    async def register_interest(self, interest_data: Dict[str, Any]) -> Interest:
        interest = Interest(
            id=0,
            name=interest_data["name"]
        )

        saved_interest = await self.interest_repo.save(interest)
        return saved_interest

    async def get_interest(self, interest_id: int) -> Optional[Interest]:
        return await self.interest_repo.find_by_id(interest_id)

    async def get_all_interests(self) -> List[Interest]:
        return await self.interest_repo.get_all()

    async def delete_interest(self, interest_id: int) -> bool:
        return await self.interest_repo.delete(interest_id)
    
    async def get_interest_name_by_id(self, interest_id: int) -> Optional[str]:
        return await self.interest_repo.get_name_by_id(interest_id)