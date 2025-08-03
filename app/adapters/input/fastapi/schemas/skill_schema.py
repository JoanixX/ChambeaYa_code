from pydantic import BaseModel, Field

class SkillCreate(BaseModel):
    name: str = Field(..., description="Name of the skill")

class SkillResponse(BaseModel):
    id: int
    name: str