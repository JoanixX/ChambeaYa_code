from pydantic import BaseModel, Field

class ExperienceDetailCreate(BaseModel):
    name: str = Field(..., description="Nombre del detalle de la experiencia")
    description: str = Field(..., description="Descripción del detalle de la experiencia")
    duration_in_months: int = Field(..., description="Duración en meses del detalle de la experiencia")

class ExperienceDetailResponse(BaseModel):
    id: int
    name: str
    description: str
    duration_in_months: int