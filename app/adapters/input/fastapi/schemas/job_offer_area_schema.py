from pydantic import BaseModel, Field

class JobOfferAreaCreate(BaseModel):
    job_offer_id: int = Field(..., description="ID of the job offer")
    area_id: int = Field(..., description="ID of the area")

class JobOfferAreaResponse(BaseModel):
    job_offer_id: int
    area_id: int