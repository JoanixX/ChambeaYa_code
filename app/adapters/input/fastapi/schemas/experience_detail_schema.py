from pydantic import BaseModel, Field, field_validator
from typing import Optional
from app.adapters.input.fastapi.validators import not_empty, positive_int

class ExperienceDetailCreate(BaseModel):
    student_id: int = Field(..., description="Student ID")
    job_offer_id: int = Field(..., description="Job Offer ID")
    name: str = Field(..., description="Name of the experience")
    description: str = Field(..., description="Description of the experience")
    duration_in_months: int = Field(..., description="Duration in months of the experience")

    @field_validator('name', 'description')
    def not_empty_fields(cls, v, info):
        return not_empty(v, info.field_name)

    @field_validator('student_id', 'job_offer_id', 'duration_in_months')
    def positive_fields(cls, v, info):
        return positive_int(v, info.field_name)

class ExperienceDetailResponse(BaseModel):
    id: int
    student_id: Optional[int]
    job_offer_id: Optional[int]
    name: str
    description: str
    duration_in_months: int