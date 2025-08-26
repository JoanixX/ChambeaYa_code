from pydantic import BaseModel, Field

class CompanyAreaCreate(BaseModel):
    company_id: int = Field(..., description="ID of the company")
    area_id: int = Field(..., description="ID of the area")

class CompanyAreaResponse(BaseModel):
    company_id: int
    area_id: int