from pydantic import BaseModel, Field, field_validator
from app.adapters.input.fastapi.validators import not_empty, positive_int

class ExternalLinkCreate(BaseModel):
    student_id: int = Field(..., description="Student ID")
    link: str = Field(..., description="Link URL")

    @field_validator('link')
    def not_empty_fields(cls, v, info):
        return not_empty(v, info.field_name)

    @field_validator('student_id')
    def positive_fields(cls, v, info):
        return positive_int(v, info.field_name)

class ExternalLinkResponse(BaseModel):
    id: int
    student_id: int
    link: str