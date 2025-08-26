from sqlalchemy.future import select
from sqlalchemy import delete
from typing import Optional

from app.domain.repositories.external_link_repository import ExternalLinkRepository
from app.domain.entities.external_link import ExternalLink
from app.adapters.output.orm.models.external_link_model import ExternalLinkModel

class ExternalLinkRepositoryImpl(ExternalLinkRepository):
    def __init__(self, session):
        self.session = session

    async def save(self, external_link: ExternalLink):
        model = ExternalLinkModel(
            student_id=external_link.student_id,
            link=external_link.link
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def find_by_id(self, external_link_id: int) -> Optional[ExternalLink]:
        result = await self.session.execute(select(ExternalLinkModel).where(ExternalLinkModel.id == external_link_id))
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

    async def find_by_student_id(self, student_id: int) -> list[ExternalLink]:
        result = await self.session.execute(select(ExternalLinkModel).where(ExternalLinkModel.student_id == student_id))
        models = result.scalars().all()
        external_links = []
        for model in models:
            external_links.append(ExternalLink(
                id=model.id,
                student_id=model.student_id,
                job_offer_id=model.job_offer_id,
                name=model.name,
                description=model.description,
                duration_in_months=model.duration_in_months,
                created_at=model.created_at,
                updated_at=model.updated_at,
                deleted_at=model.deleted_at
            ))
        return external_links

    async def get_all(self) -> list[ExternalLink]:
        result = await self.session.execute(select(ExternalLinkModel))
        models = result.scalars().all()
        external_links = []
        for model in models:
            external_links.append(
                ExternalLink(
                    id=model.id,
                    student_id=model.student_id,
                    link=model.link,
                    created_at=model.created_at,
                    updated_at=model.updated_at
                )
            )
        return external_links

    async def update(self, external_link: ExternalLink) -> Optional[ExternalLink]:
        result = await self.session.execute(select(ExternalLinkModel).where(ExternalLinkModel.id == external_link.id))
        model = result.scalar_one_or_none()
        if model:
            model.student_id = external_link.student_id
            model.link = external_link.link
            await self.session.commit()
            await self.session.refresh(model)
            return external_link
        return None

    async def delete(self, external_link_id: int):
        result = await self.session.execute(select(ExternalLinkModel).where(ExternalLinkModel.id == external_link_id))
        model = result.scalar_one_or_none()
        if not model:
            return False

        await self.session.execute(delete(ExternalLinkModel).where(ExternalLinkModel.id == external_link_id))
        await self.session.commit()
        return True