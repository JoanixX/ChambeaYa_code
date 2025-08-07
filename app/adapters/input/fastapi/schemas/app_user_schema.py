from pydantic import BaseModel, EmailStr
from app.domain.entities.app_user import UserRole

class AppUserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole
    related_id: int

    class Config:
        use_enum_values = True

class AppUserResponse(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    related_id: int
    created_at: str
    updated_at: str
    deleted_at: str = None

    class Config:
        use_enum_values = True