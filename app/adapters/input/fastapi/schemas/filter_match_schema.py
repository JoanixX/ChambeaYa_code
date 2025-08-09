from app.adapters.input.fastapi.validators import not_empty, positive_int
from pydantic import BaseModel, Field, field_validator
from typing import Optional

class FilterMatchCreate(BaseModel):
    student_id: Optional[int] = Field(None, description="ID of the student")
    job_offer_id: Optional[int] = Field(None, description="ID of the job offer")
    status: str = Field(..., description="Status of the filter match", max_length=30)
    stage: int = Field(..., description="Stage of the filter match", ge=0, le=3)

    @field_validator("job_offer_id")
    def positive_int_fields(cls, v, info):
        if v is not None:
            return positive_int(v, f'El ID de {info.field_name}')
        return v

    @field_validator("student_id")
    def positive_int_student(cls, v, info):
        if v is not None:
            return positive_int(v, f'El ID de {info.field_name}')
        return v

    @field_validator("stage")
    def stage_not_empty(cls, v, info):
        return not_empty(v, info.field_name)

class FilterMatchResponse(BaseModel):
    id: int
    student_id: Optional[int]
    job_offer_id: Optional[int]
    status: str
    stage: int