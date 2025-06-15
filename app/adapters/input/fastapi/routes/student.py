from pydantic import BaseModel, Field, EmailStr, validator
from datetime import date, datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session
from app.application.use_cases.register_student import RegisterStudentUseCase
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
import sys

class StudentCreate(BaseModel):
    name: str = Field(..., description="Name of the student")
    email: EmailStr = Field(..., description="Email address of the student")
    date_of_birth: date = Field(..., description="Date of birth of the student")
    experience_id: int = Field(..., description="Experience ID")
    enrollment_date: datetime = Field(..., description="Date when the student enrolled")
    location: str = Field(..., description="Location")
    star_skill_id: int = Field(..., description="Star skill ID")
    main_motivation_id: int = Field(..., description="Main motivation ID")
    weekly_availability: int = Field(..., description="Weekly availability")
    preferred_modality_id: int = Field(..., description="Preferred modality ID")
    career: str = Field(..., description="Career")
    academic_cycle: int = Field(..., description="Academic cycle")

    @validator('name')
    def name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v

    @validator('email')
    def email_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('El email no puede estar vacío')
        return v

    @validator('date_of_birth')
    def dob_not_in_future(cls, v):
        if v > date.today():
            raise ValueError('La fecha de nacimiento no puede ser futura')
        return v

    @validator('enrollment_date')
    def enrollment_not_in_future(cls, v):
        now = datetime.now(timezone.utc)
        if v > now:
            raise ValueError('La fecha de inscripción no puede ser futura')
        return v

    @validator('location')
    def location_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('La ubicación no puede estar vacía')
        return v

    @validator('career')
    def career_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('La carrera no puede estar vacía')
        return v

router = APIRouter()

@router.post("/register/student")
async def register_student(student: StudentCreate, session: AsyncSession = Depends(get_session)):
    try:
        use_case = RegisterStudentUseCase()
        new_student = await use_case.register(
            name=student.name,
            email=student.email,
            date_of_birth=student.date_of_birth,
            experience_id=student.experience_id,
            enrollment_date=student.enrollment_date,
            location=student.location,
            star_skill_id=student.star_skill_id,
            main_motivation_id=student.main_motivation_id,
            weekly_availability=student.weekly_availability,
            preferred_modality_id=student.preferred_modality_id,
            career=student.career,
            academic_cycle=student.academic_cycle,
            session=session
        )
        return {
            "id": new_student.id,
            "name": new_student.name,
            "email": new_student.email,
            "date_of_birth": str(new_student.date_of_birth),
            "experience_id": new_student.experience_id,
            "enrollment_date": str(new_student.enrollment_date),
            "location": new_student.location,
            "star_skill_id": new_student.star_skill_id,
            "main_motivation_id": new_student.main_motivation_id,
            "weekly_availability": new_student.weekly_availability,
            "preferred_modality_id": new_student.preferred_modality_id,
            "career": new_student.career,
            "academic_cycle": new_student.academic_cycle
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=str(e))