from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import date
from app.adapters.input.fastapi.validators import not_empty, not_in_future, in_range, positive_int, in_choices

class StudentCreate(BaseModel):
    name: str = Field(..., description="Name of the student")
    email: EmailStr = Field(..., description="Email address of the student")
    date_of_birth: date = Field(..., description="Date of birth of the student")
    experience_id: int = Field(..., description="Experience ID")
    location: str = Field(..., description="Location")
    weekly_availability: int = Field(..., description="Weekly availability")
    preferred_modality: int = Field(..., description="Preferred modality")
    career: str = Field(..., description="Career")
    academic_cycle: int = Field(..., description="Academic cycle")
    main_motivation: str = Field(..., description="Main motivation")
    description: str = Field(..., description="Description")

    @field_validator('name', 'location', 'career', 'main_motivation', 'description')
    def not_empty_fields(cls, v, info):
        return not_empty(v, info.field_name)

    @field_validator('date_of_birth')
    def dob_not_in_future(cls, v, info):
        return not_in_future(v, 'La fecha de nacimiento')

    @field_validator('weekly_availability')
    def weekly_availability_valid(cls, v, info):
        return in_range(v, 1, 40, 'La disponibilidad semanal')

    @field_validator('academic_cycle')
    def academic_cycle_valid(cls, v, info):
        return in_range(v, 1, 12, 'El ciclo académico')

    @field_validator('experience_id')
    def experience_id_valid(cls, v, info):
        return positive_int(v, 'El ID de experiencia')

    @field_validator('preferred_modality')
    def preferred_modality_valid(cls, v, info):
        return in_choices(v, [1, 2, 3], 'La modalidad preferida')
    
    @field_validator('email')
    def valid_email(cls, v):
        return EmailStr._validate(v)
    
class StudentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    date_of_birth: date
    experience_id: int
    location: str
    weekly_availability: int
    preferred_modality: int
    career: str
    academic_cycle: int
    main_motivation: str
    description: str
    created_at: str
    updated_at: str
    deleted_at: str = None