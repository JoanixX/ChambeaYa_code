from pydantic import BaseModel, Field

class AreaCreate(BaseModel):
    name: str = Field(..., description="Name of the area")

class AreaResponse(BaseModel):
    id: int
    name: str