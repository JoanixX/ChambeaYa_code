from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session
from app.adapters.output.orm.repositories.job_offer_repository_impl import (
    get_all_job_offers_impl,
    get_job_offer_by_id_impl,
    create_job_offer_impl,
    update_job_offer_impl,
    delete_job_offer_impl
)
from app.adapters.output.orm.repositories.company_repository_impl import CompanyRepositoryImpl
from app.domain.entities.job_offer import JobOffer
from typing import List
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

router = APIRouter()

class JobOfferCreate(BaseModel):
    company_id: int = Field(..., description="ID of the company")
    title: str = Field(..., description="Title of the job offer")
    description: str = Field(..., description="Description")
    required_hours: int = Field(..., description="Required hours")
    approximated_salary: int = Field(..., description="Approximated salary")
    duration: int = Field(..., description="Duration")
    start_date: date = Field(..., description="Start date")
    area_id: int = Field(..., description="Area ID")
    experience_id: int = Field(..., description="Experience ID")
    modality: int = Field(..., description="Modality")
    requirements: Optional[str] = Field(None, description="Requirements")
    embedding: Optional[dict] = Field(None, description="Embedding")

@router.get("/job_offer/all", response_model=List[dict], tags=["Job Offer"])
async def get_all_job_offers_endpoint(session: AsyncSession = Depends(get_session)):
    job_offers: List[JobOffer] = await get_all_job_offers_impl(session)
    result = []
    for j in job_offers:
        result.append({
            "id": j.id,
            "company_id": j.company_id,
            "title": j.title,
            "description": j.description,
            "required_hours": j.required_hours,
            "approximated_salary": j.approximated_salary,
            "duration": j.duration,
            "start_date": j.start_date.isoformat() if j.start_date else None,
            "area_id": j.area_id,
            "experience_id": j.experience_id,
            "modality": j.modality,
            "requirements": j.requirements,
            "embedding": j.embedding
        })
    return result

@router.get("/job_offer/{job_offer_id}", response_model=dict, tags=["Job Offer"])
async def get_job_offer_by_id_endpoint(job_offer_id: int, session: AsyncSession = Depends(get_session)):
    job_offer = await get_job_offer_by_id_impl(session, job_offer_id)
    if not job_offer:
        raise HTTPException(status_code=404, detail="Job offer not found")
    return {
        "id": job_offer.id,
        "company_id": job_offer.company_id,
        "title": job_offer.title,
        "description": job_offer.description,
        "required_hours": job_offer.required_hours,
        "approximated_salary": job_offer.approximated_salary,
        "duration": job_offer.duration,
        "start_date": job_offer.start_date.isoformat() if job_offer.start_date else None,
        "area_id": job_offer.area_id,
        "experience_id": job_offer.experience_id,
        "modality": job_offer.modality,
        "requirements": job_offer.requirements,
        "embedding": job_offer.embedding
    }

@router.post("/job_offer", response_model=dict, tags=["Job Offer"])
async def create_job_offer_endpoint(job_offer: JobOfferCreate, session: AsyncSession = Depends(get_session)):
    company_id = job_offer.company_id
    company_repo = CompanyRepositoryImpl(session)
    company = await company_repo.find_by_id(company_id)
    if not company:
        raise HTTPException(status_code=403, detail="Only a valid company can create a job offer")
    job_offer_entity = JobOffer(id=None, **job_offer.dict())
    created = await create_job_offer_impl(session, job_offer_entity)
    return {
        "id": created.id,
        "company_id": created.company_id,
        "title": created.title,
        "description": created.description,
        "required_hours": created.required_hours,
        "approximated_salary": created.approximated_salary,
        "duration": created.duration,
        "start_date": created.start_date.isoformat() if created.start_date else None,
        "area_id": created.area_id,
        "experience_id": created.experience_id,
        "modality": created.modality,
        "requirements": created.requirements,
        "embedding": created.embedding
    }

@router.put("/job_offer/{job_offer_id}", response_model=dict, tags=["Job Offer"])
async def update_job_offer_endpoint(job_offer_id: int, job_offer: JobOfferCreate, session: AsyncSession = Depends(get_session)):
    job_offer_entity = JobOffer(id=job_offer_id, **job_offer.dict())
    updated = await update_job_offer_impl(session, job_offer_entity)
    if not updated:
        raise HTTPException(status_code=404, detail="Job offer not found")
    return {
        "id": updated.id,
        "company_id": updated.company_id,
        "title": updated.title,
        "description": updated.description,
        "required_hours": updated.required_hours,
        "approximated_salary": updated.approximated_salary,
        "duration": updated.duration,
        "start_date": updated.start_date.isoformat() if updated.start_date else None,
        "area_id": updated.area_id,
        "experience_id": updated.experience_id,
        "modality": updated.modality,
        "requirements": updated.requirements,
        "embedding": updated.embedding
    }

@router.delete("/job_offer/{job_offer_id}", response_model=dict, tags=["Job Offer"])
async def delete_job_offer_endpoint(job_offer_id: int, session: AsyncSession = Depends(get_session)):
    deleted = await delete_job_offer_impl(session, job_offer_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Job offer not found")
    return {"detail": "Job offer deleted"}
