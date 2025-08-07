from pydantic import BaseModel, Field

class AreaCreate(BaseModel):
    name: str = Field(..., description="Nombre del área")

class AreaResponse(BaseModel):
    id: int = Field(..., description="ID del área")
    name: str = Field(..., description="Nombre del área")