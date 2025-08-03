from pydantic import BaseModel, Field

class StudentSkillCreate(BaseModel):
    student_id: int = Field(..., description="ID del estudiante")
    skill_id: int = Field(..., description="ID de la habilidad")

class StudentSkillResponse(BaseModel):
    student_id: int
    skill_id: int