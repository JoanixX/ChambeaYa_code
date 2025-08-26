from pydantic import BaseModel, Field, field_validator
from typing import Optional
from app.adapters.input.fastapi.validators import not_empty, in_range, in_choices

class StudentCreate(BaseModel):
    weekly_availability: int = Field(..., description="Weekly availability")
    preferred_modality: int = Field(..., description="Preferred modality")
    career: str = Field(..., description="Career")
    academic_cycle: int = Field(..., description="Academic cycle")

    @field_validator('career')
    def not_empty_fields(cls, v, info):
        return not_empty(v, info.field_name)

    @field_validator('weekly_availability')
    def weekly_availability_valid(cls, v, info):
        return in_range(v, 1, 40, 'La disponibilidad semanal')

    @field_validator('academic_cycle')
    def academic_cycle_valid(cls, v, info):
        return in_range(v, 1, 12, 'El ciclo académico')

    @field_validator('preferred_modality')
    def preferred_modality_valid(cls, v, info):
        return in_choices(v, [1, 2, 3], 'La modalidad preferida')
    
class StudentResponse(BaseModel):
    id: int
    weekly_availability: int
    preferred_modality: int
    career: str
    academic_cycle: int
    embedding: Optional[dict] = None