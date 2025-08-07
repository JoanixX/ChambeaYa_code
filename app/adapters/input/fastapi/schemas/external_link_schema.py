from pydantic import BaseModel, Field

class ExternalLinkCreate(BaseModel):
    student_id: int = Field(..., description="ID of the student")
    link: str = Field(..., description="External link URL")

class ExternalLinkResponse(BaseModel):
    id: int
    student_id: int
    link: str
    created_at: str
    updated_at: str