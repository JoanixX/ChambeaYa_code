from pydantic import BaseModel, Field, EmailStr, validator
from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session
from app.application.use_cases.register_student import RegisterStudentUseCase
from app.adapters.output.orm.repositories.student_repository_impl import StudentRepositoryImpl
from app.domain.services.student_profile_evaluator import StudentProfileEvaluator
from app.application.ports.register_student_port import RegisterStudentPort
from fastapi.responses import JSONResponse

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
    main_motivation: str = Field(..., description="Main motivation")
    description: str = Field(..., description="Description")

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

class StudentPortImpl(RegisterStudentPort):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.student_repo = StudentRepositoryImpl(session)

    async def register_student(self, student):
        return await self.student_repo.save(student)

    async def validate_student_data(self, student_data: dict) -> bool:
        # Validaciones básicas
        required_fields = ['name', 'email', 'date_of_birth', 'experience_id', 'location', 
                         'weekly_availability', 'preferred_modality', 'career', 'academic_cycle', 
                         'main_motivation', 'description']
        
        for field in required_fields:
            if field not in student_data or not student_data[field]:
                return False
        
        # Validaciones específicas
        if student_data['weekly_availability'] <= 0 or student_data['weekly_availability'] > 40:
            return False
        
        if student_data['academic_cycle'] <= 0 or student_data['academic_cycle'] > 12:
            return False
        
        return True

    async def check_email_exists(self, email: str) -> bool:
        student = await self.student_repo.find_by_email(email)
        return student is not None

@router.post("/register/student")
async def register_student(student: StudentCreate, session: AsyncSession = Depends(get_session)):
    try:
        # Crear adaptadores
        student_port = StudentPortImpl(session)
        student_evaluator = StudentProfileEvaluator(student_port.student_repo, student_port)
        
        # Crear caso de uso
        use_case = RegisterStudentUseCase(student_port, student_evaluator)
        
        # Ejecutar caso de uso
        result = await use_case.execute(student.dict())
        
        return JSONResponse(content=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/student/{student_id}/profile")
async def get_student_profile(student_id: int, session: AsyncSession = Depends(get_session)):
    try:
        student_repo = StudentRepositoryImpl(session)
        student_evaluator = StudentProfileEvaluator(student_repo, None)
        
        evaluation = await student_evaluator.evaluate_student_profile(student_id)
        
        return JSONResponse(content=evaluation)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")