from sqlalchemy.future import select
from sqlalchemy import delete
from typing import Optional
from datetime import datetime

from app.adapters.output.orm.models.external_link_model import ExternalLinkModel
from app.domain.entities.external_link import ExternalLink
from app.domain.repositories.external_link_repository import ExternalLinkRepository

class ExternalLinkRepositoryImpl(ExternalLinkRepository):
    def __init__(self, session):
        self.session = session

    async def save (self, external_link: ExternalLink) -> ExternalLink:
        now = datetime.utcnow()
        model = ExternalLinkModel(
            student_id=external_link.student_id,
            link=external_link.link,
            created_at=now,
            updated_at=now
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model
    
    async def find_by_id(self, link_id: int) -> Optional[ExternalLink]:
        result = await self.session.execute(select(ExternalLinkModel).where(ExternalLinkModel.id == link_id))
        model = result.scalar_one_or_none()
        if model:
            return ExternalLink(
                id=model.id,
                student_id=model.student_id,
                link=model.link,
                created_at=model.created_at,
                updated_at=model.updated_at
            )
        return None
    
    async def get_all(self) -> list[ExternalLink]:
        result = await self.session.execute(select(ExternalLinkModel))
        models = result.scalars().all()
        links = []
        for model in models:
            links.append(
                ExternalLink(
                    id=model.id,
                    student_id=model.student_id,
                    link=model.link,
                    created_at=model.created_at,
                    updated_at=model.updated_at
                )
            )
        return links
    
    async def update(self, external_link_id: int, new_link: str) -> Optional[ExternalLink]:
        result = await self.session.execute(select(ExternalLinkModel).where(ExternalLinkModel.id == external_link_id))
        model = result.scalar_one_or_none()
        if model:
            model.link = new_link
            model.updated_at = datetime.utcnow()
            self.session.add(model)
            await self.session.commit()
            await self.session.refresh(model)
            return ExternalLink(
                id=model.id,
                student_id=model.student_id,
                link=model.link,
                created_at=model.created_at,
                updated_at=model.updated_at
            )
        return None

    async def delete(self, link_id: int) -> bool:
        result = await self.session.execute(select(ExternalLinkModel).where(ExternalLinkModel.id == link_id))
        model = result.scalar_one_or_none()
        if not model:
            return False

        await self.session.execute(delete(ExternalLinkModel).where(ExternalLinkModel.id == link_id))
        await self.session.commit()
        return True
    
    async def get_link_by_id(self, link_id: int) -> Optional[str]:
        result = await self.session.execute(select(ExternalLinkModel.link).where(ExternalLinkModel.id == link_id))
        link = result.scalar_one_or_none()
        return link if link else None