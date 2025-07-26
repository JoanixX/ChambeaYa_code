from pydantic import BaseModel, Field, EmailStr, validator
from app.adapters.input.fastapi.validators import not_empty, not_in_future, in_range, positive_int, in_choices
from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session
from app.application.use_cases.register_student import RegisterStudentUseCase
from app.adapters.output.orm.repositories.student_repository_impl import StudentRepositoryImpl
from app.domain.services.register_student_service import RegisterStudentService
from app.application.ports.register_student_port import RegisterStudentPort
from app.adapters.output.orm.models.experience_detail_model import ExperienceDetailModel
from fastapi.responses import JSONResponse
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

    from pydantic import field_validator

    @field_validator('name', 'location', 'career', 'main_motivation', 'description')
    def not_empty_fields(cls, v, info):
        return not_empty(v, info.field_name)

    @field_validator('date_of_birth')
    def dob_not_in_future(cls, v, info):
        return not_in_future(v, 'La fecha de nacimiento')

    @field_validator('weekly_availability')
    def weekly_availability_valid(cls, v, info):
        return in_range(v, 1, 40, 'La disponibilidad semanal')

    @field_validator('academic_cycle')
    def academic_cycle_valid(cls, v, info):
        return in_range(v, 1, 12, 'El ciclo académico')

    @field_validator('experience_id')
    def experience_id_valid(cls, v, info):
        return positive_int(v, 'El ID de experiencia')

    @field_validator('preferred_modality')
    def preferred_modality_valid(cls, v, info):
        return in_choices(v, [1, 2, 3], 'La modalidad preferida')

router = APIRouter()

class StudentPortImpl(RegisterStudentPort):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.student_repo = StudentRepositoryImpl(session)

    async def register_student(self, student):
        return await self.student_repo.save(student)

    async def validate_student_data(self, student_data: dict) -> bool:
        logger.info(f"Validando datos del estudiante: {student_data}")
        
        # Validaciones básicas
        required_fields = ['name', 'email', 'date_of_birth', 'location', 'experience_id',
                         'weekly_availability', 'preferred_modality', 'career', 'academic_cycle', 
                         'main_motivation', 'description']
        
        for field in required_fields:
            if field not in student_data or not student_data[field]:
                logger.error(f"Campo faltante o vacío: {field}")
                return False
        
        # Validaciones específicas
        if student_data['weekly_availability'] <= 0 or student_data['weekly_availability'] > 40:
            logger.error(f"weekly_availability inválido: {student_data['weekly_availability']}")
            return False
        
        if student_data['academic_cycle'] <= 0 or student_data['academic_cycle'] > 12:
            logger.error(f"academic_cycle inválido: {student_data['academic_cycle']}")
            return False
        
        logger.info("Validación exitosa")
        return True

    async def check_email_exists(self, email: str) -> bool:
        student = await self.student_repo.find_by_email(email)
        return student is not None

@router.post("/register/student", tags=["Estudiante"])
async def register_student(request: Request, student: StudentCreate, session: AsyncSession = Depends(get_session)):
    try:
        # Log del body recibido para debug
        body = await request.body()
        logger.info(f"Body recibido: {body.decode()}")
        
        logger.info(f"Iniciando registro de estudiante: {student.email}")
        
        # Crear adaptadores
        student_port = StudentPortImpl(session)
        student_repo = StudentRepositoryImpl(session)
        register_student_service = RegisterStudentService(student_repo, student_port)
        
        # Crear caso de uso
        use_case = RegisterStudentUseCase(student_port, register_student_service)
        
        # Ejecutar caso de uso
        logger.info("Ejecutando caso de uso...")
        result = await use_case.execute(student.dict())
        
        logger.info(f"Estudiante registrado exitosamente: {result}")
        return JSONResponse(content=result)
    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error interno del servidor: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/student/{student_id}", response_model=dict, tags=["Estudiante"])
async def get_student_by_id(student_id: int, session: AsyncSession = Depends(get_session)):
    student_repo = StudentRepositoryImpl(session)
    student = await student_repo.find_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student.__dict__

@router.get("/student/all", response_model=list, tags=["Estudiante"])
async def get_all_students(session: AsyncSession = Depends(get_session)):
    student_repo = StudentRepositoryImpl(session)
    students = await student_repo.get_all()
    return [s.__dict__ for s in students]

@router.put("/student/{student_id}", response_model=dict, tags=["Estudiante"])
async def update_student(student_id: int, student: StudentCreate, session: AsyncSession = Depends(get_session)):
    student_repo = StudentRepositoryImpl(session)
    updated = await student_repo.update(student_id, student.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated.__dict__

@router.delete("/student/{student_id}", response_model=dict, tags=["Estudiante"])
async def delete_student(student_id: int, session: AsyncSession = Depends(get_session)):
    student_repo = StudentRepositoryImpl(session)
    deleted = await student_repo.delete(student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"detail": "Student deleted"}