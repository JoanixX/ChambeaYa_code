from pydantic import BaseModel, Field

class InterestCreate(BaseModel):
    name: str = Field(..., description="Name of the interest")

class InterestResponse(BaseModel):
    id: int
    name: str