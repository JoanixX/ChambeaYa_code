from sqlalchemy.future import select
from sqlalchemy import delete
from typing import Optional
from app.adapters.output.orm.models.interest_model import InterestModel
from app.domain.entities.interest import Interest
from app.domain.repositories.interest_repository import InterestRepository

class InterestRepositoryImpl(InterestRepository):
    def __init__(self, session):
        self.session = session
    
    async def save(self, interest: Interest):
        model = InterestModel(
            name=interest.name
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model
    
    async def find_by_id(self, interest_id: int) -> Optional[Interest]:
        result = await self.session.execute(select(InterestModel).where(InterestModel.id == interest_id))
        model = result.scalar_one_or_none()
        if model:
            return Interest(
                id=model.id,
                name=model.name
            )
        return None
    
    async def get_all(self) -> list[Interest]:
        result = await self.session.execute(select(InterestModel))
        models = result.scalars().all()
        interests = []
        for model in models:
            interests.append(
                Interest(
                    id=model.id,
                    name=model.name
                )
            )
        return interests
    
    async def delete(self, interest_id: int) -> bool:
        result = await self.session.execute(select(InterestModel).where(InterestModel.id == interest_id))
        model = result.scalar_one_or_none()
        if not model:
            return False

        await self.session.execute(delete(InterestModel).where(InterestModel.id == interest_id))
        await self.session.commit()
        return True
    
    async def get_name_by_id(self, interest_id: int) -> Optional[str]:
        result = await self.session.execute(select(InterestModel.name).where(InterestModel.id == interest_id))
        name = result.scalar_one_or_none()
        return name if name else None