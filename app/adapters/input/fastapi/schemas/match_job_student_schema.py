from pydantic import BaseModel, Field
from typing import Optional

class MatchJobStudentRequest(BaseModel):
    student_id: int = Field(..., description="ID del estudiante")
    job_offer_id: int = Field(..., description="ID de la oferta de trabajo")
    skills: Optional[list[int]] = Field(None, description="Lista de IDs de habilidades del estudiante")
    experience_details: Optional[list[int]] = Field(None, description="Lista de IDs de detalles de experiencia del estudiante")

class MatchJobStudentResponse(BaseModel):
    student_id: int
    job_offer_id: int
    score: float
    match_date: str
    rank: int
    updated_at: str
    deleted_at: str = None