from pydantic import BaseModel, Field, EmailStr, validator
from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session
from app.application.use_cases.register_student import RegisterStudentUseCase
from fastapi.responses import JSONResponse
from .jwt_utils import create_access_token, verify_password
from sqlalchemy.future import select
from app.domain.entities.student import Student

class StudentCreate(BaseModel):
    name: str = Field(..., description="Name of the student")
    email: EmailStr = Field(..., description="Email address of the student")
    date_of_birth: date = Field(..., description="Date of birth of the student")
    experience_id: int = Field(..., description="Experience ID")
    location: str = Field(..., description="Location")
    weekly_availability: int = Field(..., description="Weekly availability")
    preferred_modality: int = Field(..., description="Preferred modality")
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
    use_case = RegisterStudentUseCase()
    new_student = await use_case.register(
        name=student.name,
        email=student.email,
        date_of_birth=student.date_of_birth,
        experience_id=student.experience_id,
        location=student.location,
        weekly_availability=student.weekly_availability,
        preferred_modality=student.preferred_modality,
        career=student.career,
        academic_cycle=student.academic_cycle,
        session=session
    )
    return JSONResponse(content={"id": new_student.id})