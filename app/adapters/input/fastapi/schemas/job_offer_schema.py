from app.adapters.input.fastapi.validators import not_empty, start_date_future, positive_int, in_choices
from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import Optional

class JobOfferCreate(BaseModel):
    company_id: int = Field(..., description="ID of the company")
    title: str = Field(..., description="Title of the job offer")
    description: str = Field(..., description="Description")
    required_hours: int = Field(..., description="Required hours")
    approximated_salary: int = Field(..., description="Approximated salary")
    duration: int = Field(..., description="Duration")
    start_date: date = Field(..., description="Start date")
    area_id: int = Field(..., description="Area ID")
    experience_id: int = Field(..., description="Experience ID")
    modality: int = Field(..., description="Modality")

    @field_validator("start_date")
    def start_date_validator(cls, v, info):
        return start_date_future(v, 'La fecha de inicio no puede ser en el pasado')
    
    @field_validator("required_hours", "approximated_salary", "duration")
    def not_empty_fields(cls, v, info):
            return not_empty(v, info.field_name)
    
    @field_validator('modality')
    def preferred_modality_valid(cls, v, info):
        return in_choices(v, [1, 2, 3], 'La modalidad preferida')
    
    @field_validator('experience_id')
    def experience_id_valid(cls, v, info):
        return positive_int(v, 'El ID de experiencia')
    
    @field_validator('area_id')
    def area_id_valid(cls, v, info):
        return positive_int(v, 'El ID del area')

class JobOfferResponse(BaseModel):
    id: int
    company_id: int
    title: str
    description: str
    required_hours: int
    approximated_salary: int
    duration: int
    start_date: date
    area_id: int
    experience_id: int 
    modality: int
    embedding: Optional[dict] = None