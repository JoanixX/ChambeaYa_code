from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session
from app.adapters.output.orm.repositories.skill_repository_impl import (
    get_all_skills_impl,
    get_skill_by_id_impl,
    create_skill_impl,
    update_skill_impl,
    delete_skill_impl
)
from app.domain.entities.skill import Skill
from typing import List, Optional
from pydantic import BaseModel, Field

router = APIRouter()

class SkillCreate(BaseModel):
    name: str = Field(..., description="Name of the skill")

@router.get("/skill/all", response_model=List[dict], tags=["Skill"])
async def get_all_skills_endpoint(session: AsyncSession = Depends(get_session)):
    skills: List[Skill] = await get_all_skills_impl(session)
    result = []
    for skill in skills:
        result.append({
            "id": skill.id,
            "name": skill.name
        })
    return result

@router.get("/skill/{skill_id}", response_model=dict, tags=["Skill"])
async def get_skill_by_id_endpoint(skill_id: int, session: AsyncSession = Depends(get_session)):
    skill = await get_skill_by_id_impl(session, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill no encontrada")
    
    return {
        "id": skill.id,
        "name": skill.name
    }

@router.post("/skill", response_model=dict, tags=["Skill"])
async def create_skill_endpoint(skill: SkillCreate, session: AsyncSession = Depends(get_session)):
    skill_entity = Skill(id=None, name=skill.name)
    created_skill = await create_skill_impl(session, skill_entity)
    
    return {
        "id": created_skill.id,
        "name": created_skill.name
    }

@router.put("/skill/{skill_id}", response_model=dict, tags=["Skill"])
async def update_skill_endpoint(skill_id: int, skill: SkillCreate, session: AsyncSession = Depends(get_session)):
    existing_skill = await get_skill_by_id_impl(session, skill_id)
    if not existing_skill:
        raise HTTPException(status_code=404, detail="Skill no encontrada")
    
    updated_skill = Skill(id=skill_id, name=skill.name)
    updated_skill = await update_skill_impl(session, updated_skill)
    
    return {
        "id": updated_skill.id,
        "name": updated_skill.name
    }

@router.delete("/skill/{skill_id}", response_model=dict, tags=["Skill"])
async def delete_skill_endpoint(skill_id: int, session: AsyncSession = Depends(get_session)):
    deleted = await delete_skill_impl(session, skill_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Skill no encontrada")
    return {"detail": "Skill eliminada"}