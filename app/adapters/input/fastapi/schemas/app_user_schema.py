from pydantic import BaseModel, EmailStr
from app.domain.entities.app_user import UserRole


class AppUserCreate(BaseModel):
    email: EmailStr
    password: str
    dni: str
    role: UserRole
    related_id: int

    class Config:
        use_enum_values = True

class AppUserResponse(BaseModel):
    id: int
    email: EmailStr
    dni: str
    role: UserRole
    related_id: int

    class Config:
        use_enum_values = True

class LoginCreate(BaseModel):
    email: EmailStr
    password: str