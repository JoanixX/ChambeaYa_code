from pydantic import BaseModel, Field

class JobOfferRequiredSkillCreate(BaseModel):
    job_offer_id: int = Field(..., description="ID de la oferta de trabajo")
    skill_id: int = Field(..., description="ID de la habilidad")

class JobOfferRequiredSkillResponse(BaseModel):
    job_offer_id: int
    skill_id: int
