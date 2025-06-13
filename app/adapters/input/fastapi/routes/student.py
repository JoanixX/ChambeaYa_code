from pydantic import BaseModel, Field, EmailStr, validator
from datetime import date, datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session
from app.application.use_cases.register_student import RegisterStudentUseCase

class StudentCreate(BaseModel):
    name: str = Field(..., description="Name of the student")
    email: EmailStr = Field(..., description="Email address of the student")
    date_of_birth: date = Field(..., description="Date of birth of the student")
    enrollment_date: datetime = Field(..., description="Date when the student enrolled")

    @validator('name')
    def name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre no puede estar vacío')
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

router = APIRouter()

@router.post("/register/student")
async def register_student(student: StudentCreate, session: AsyncSession = Depends(get_session)):
    try:
        use_case = RegisterStudentUseCase()
        new_student = await use_case.register(
            name=student.name,
            email=student.email,
            date_of_birth=student.date_of_birth,
            enrollment_date=student.enrollment_date,
            session=session
        )
        return {
            "id": new_student.id,
            "name": new_student.name,
            "email": new_student.email,
            "date_of_birth": str(new_student.date_of_birth),
            "enrollment_date": str(new_student.enrollment_date)
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=str(e))