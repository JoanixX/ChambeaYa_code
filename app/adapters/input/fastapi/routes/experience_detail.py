from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session
from app.adapters.output.orm.models.experience_detail_model import ExperienceDetailModel
from sqlalchemy.future import select

router = APIRouter()

@router.get("/experience_detail", tags=["ExperienceDetail"])
async def list_experience_details(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(ExperienceDetailModel))
    experience_details = result.scalars().all()
    return [
        {
            "id": exp.id,
            "name": exp.name,
            "description": exp.description,
            "duration_in_months": exp.duration_in_months
        }
        for exp in experience_details
    ]
