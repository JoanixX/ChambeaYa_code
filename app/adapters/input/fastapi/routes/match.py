from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.infraestructure.database.connection import get_session
from app.domain.entities.match_job_student import MatchJobStudent
from app.domain.entities.student import Student
from app.domain.entities.company import Company
from app.domain.entities.job_offer import JobOffer

router = APIRouter()

class MatchResult(BaseModel):
    student_id: int
    company_id: int
    score: float
    student_name: str
    company_name: str

@router.get("/matches/ranking", response_model=List[MatchResult])
async def get_matches_ranking(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(MatchJobStudent, Student, JobOffer, Company)
        .join(Student, MatchJobStudent.student_id == Student.id)
        .join(JobOffer, MatchJobStudent.job_offer_id == JobOffer.id)
        .join(Company, JobOffer.company_id == Company.id)
    )
    matches = []
    for match, student, job_offer, company in result.all():
        matches.append(MatchResult(
            student_id=student.id,
            company_id=company.id,
            score=float(match.score) if match.score is not None else 0.0,
            student_name=student.name,
            company_name=company.name
        ))
    return matches