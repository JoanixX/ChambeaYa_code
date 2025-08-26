from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional
from app.domain.entities.app_user import UserRole

class AppUserCreate(BaseModel):
    email: EmailStr = Field(..., description="Correo electrónico del usuario")
    password: str = Field(..., description="Contraseña del usuario")
    dni: str = Field(..., description="DNI del usuario")
    name: str = Field(..., description="Nombre del usuario")
    location: str = Field(..., description="Ubicación del usuario")
    role: UserRole = Field(..., description="Rol del usuario")
    related_id: int = Field(..., description="ID relacionado (por ejemplo, ID de estudiante o empresa)")
    cv_url: Optional[str] = Field(None, description="URL del CV del estudiante", max_length=512, example="")
    date_of_birth: Optional[str] = Field(None, description="Fecha de nacimiento del estudiante", example="")
    main_motivation: Optional[str] = Field(None, description="Motivación principal del estudiante", example="")
    description: Optional[str] = Field(None, description="Descripción del estudiante", example="")
    ruc: Optional[str] = Field(None, description="RUC de la compañía", example="")

    @model_validator(mode="after")
    def check_role_fields(cls, values):
        role = values.role
        if role == UserRole.student:
            missing = []
            for field in ["date_of_birth", "main_motivation", "description"]:
                if not getattr(values, field, None):
                    missing.append(field)
            if missing:
                raise ValueError(f"Campos requeridos para estudiante: {', '.join(missing)}")
        if role == UserRole.company:
            if not values.ruc:
                raise ValueError("ruc es requerido para compañías")
        return values
    class Config:
        use_enum_values = True

class AppUserResponse(BaseModel):
    id: int
    email: EmailStr
    dni: str
    name: str
    location: str
    role: UserRole
    related_id: int
    cv_url: Optional[str] = None
    date_of_birth: Optional[str] = None
    main_motivation: Optional[str] = None
    description: Optional[str] = None
    ruc: Optional[str] = None

    class Config:
        use_enum_values = True

class LoginCreate(BaseModel):
    email: EmailStr
    password: str