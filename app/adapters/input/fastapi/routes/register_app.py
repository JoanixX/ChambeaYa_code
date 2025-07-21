from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.infraestructure.database.connection import get_session
from app.adapters.output.orm.models.app_user_model import AppUserModel
from app.domain.entities.app_user import UserRole
from pydantic import BaseModel, EmailStr
from .jwt_utils import get_password_hash

router = APIRouter()

class UserRegisterInput(BaseModel):
    email: EmailStr
    password: str
    role: UserRole
    related_id: int

@router.post("/register/user")
async def register_user(user: UserRegisterInput, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(AppUserModel).where(AppUserModel.email == user.email))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    password_hash = get_password_hash(user.password)
    new_user = AppUserModel(
        email=user.email,
        password_hash=password_hash,
        role=user.role.value,
        related_id=user.related_id
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return {"id": new_user.id, "email": new_user.email, "role": new_user.role, "related_id": new_user.related_id}