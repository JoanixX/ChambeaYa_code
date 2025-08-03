from pydantic import BaseModel, EmailStr
from app.domain.entities.app_user import UserRole

class AppUserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole
    related_id: int

class AppUserResponse(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    related_id: int