from pydantic import BaseModel, Field, EmailStr, field_validator
from app.adapters.input.fastapi.validators import not_empty, positive_int

class CompanyCreate(BaseModel):
    RUC: str = Field(..., description="RUC de la empresa")
    name: str = Field(..., description="Nombre de la empresa")
    location: str = Field(..., description="Ubicación de la empresa")
    industry: str = Field(..., description="Industria de la empresa")
    area_id: int = Field(..., description="ID del área")
    contact_name: str = Field(..., description="Nombre del contacto")
    email: str = Field(..., description="Correo electrónico de la empresa")
    company_culture: str = Field(..., description="Cultura de la empresa")

    @field_validator('name', 'RUC', 'industry', 'company_culture', 'contact_name', 'location')
    def not_empty_fields(cls, v, info):
        return not_empty(v, info.field_name)
    
    @field_validator('email')
    def valid_email(cls, v):
        return EmailStr._validate(v)
    
    @field_validator('area_id')
    def experience_id_valid(cls, v, info):
        return positive_int(v, 'El ID del area')
    
class CompanyResponse(BaseModel):
    id: int
    RUC: str
    name: str
    location: str
    industry: str
    area_id: int
    contact_name: str
    email: EmailStr
    company_culture: str
    created_at: str
    updated_at: str
    deleted_at: str = None