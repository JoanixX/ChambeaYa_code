from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.infraestructure.database.connection import get_session
from app.adapters.output.orm.models.area_model import AreaModel

router = APIRouter()

@router.get("/area/all", response_model=list, tags=["Area"])
async def get_all_areas(session: AsyncSession = Depends(get_session)):
    try:
        result = await session.execute(select(AreaModel))
        areas = result.scalars().all()
        return [{"id": area.id, "name": area.name} for area in areas]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")