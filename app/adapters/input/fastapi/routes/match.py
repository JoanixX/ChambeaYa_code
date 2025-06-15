from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class MatchResult(BaseModel):
    student_id: int
    company_id: int
    score: float
    student_name: str
    company_name: str

@router.get("/matches/ranking", response_model=List[MatchResult])
async def get_matches_ranking():
    matches = [
        MatchResult(student_id=1, company_id=1, score=0.92, student_name="Juan Perez", company_name="Empresa A"),
        MatchResult(student_id=2, company_id=1, score=0.85, student_name="Ana Ruiz", company_name="Empresa A"),
        MatchResult(student_id=3, company_id=2, score=0.78, student_name="Luis Torres", company_name="Empresa B"),
        MatchResult(student_id=1, company_id=2, score=0.65, student_name="Juan Perez", company_name="Empresa B"),
    ]
    return matches