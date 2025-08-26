from pydantic import BaseModel, Field, field_validator
from app.adapters.input.fastapi.validators import not_empty

class CompanyCreate(BaseModel):
    name: str = Field(..., description="Nombre de la empresa")
    industry: str = Field(..., description="Industria de la empresa")
    company_culture: str = Field(..., description="Cultura de la empresa")

    @field_validator('name', 'industry', 'company_culture')
    def not_empty_fields(cls, v, info):
        return not_empty(v, info.field_name)
    
class CompanyResponse(BaseModel):
    id: int
    name: str
    industry: str
    company_culture: str