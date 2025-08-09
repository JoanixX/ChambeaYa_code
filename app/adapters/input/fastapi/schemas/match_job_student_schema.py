from app.adapters.input.fastapi.validators import not_empty, positive_int
from pydantic import BaseModel, Field, field_validator
from typing import Optional

class MatchJobStudentCreate(BaseModel):
    student_id: int = Field(..., description="ID del estudiante")
    job_offer_id: int = Field(..., description="ID de la oferta de trabajo")
    score: float = Field(..., description="Puntaje de similitud")
    match_date: str = Field(..., description="Fecha del emparejamiento")
    rank: int = Field(..., description="Rango del emparejamiento")

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

    @field_validator("rank")
    def stage_not_empty(cls, v, info):
        return not_empty(v, info.field_name)

class MatchJobStudentResponse(BaseModel):
    id: Optional[int] = None
    student_id: int
    job_offer_id: int
    score: float
    match_date: str
    rank: int
