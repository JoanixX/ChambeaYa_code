from pydantic import BaseModel, Field, EmailStr, validator
from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session
from app.application.use_cases.register_student import RegisterStudentUseCase
from app.adapters.output.orm.repositories.student_repository_impl import StudentRepositoryImpl
from app.domain.services.register_student_service import RegisterStudentService
from app.application.ports.register_student_port import RegisterStudentPort
from fastapi.responses import JSONResponse
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StudentCreate(BaseModel):
    name: str = Field(..., description="Name of the student")
    email: EmailStr = Field(..., description="Email address of the student")
    date_of_birth: date = Field(..., description="Date of birth of the student")
    experience_id: Optional[int] = Field(None, description="Experience ID (optional)")
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

    @validator('weekly_availability')
    def weekly_availability_valid(cls, v):
        if v <= 0 or v > 40:
            raise ValueError('La disponibilidad semanal debe estar entre 1 y 40 horas')
        return v

    @validator('academic_cycle')
    def academic_cycle_valid(cls, v):
        if v <= 0 or v > 12:
            raise ValueError('El ciclo académico debe estar entre 1 y 12')
        return v

    @validator('experience_id')
    def experience_id_valid(cls, v):
        if v is not None and v <= 0:
            raise ValueError('El ID de experiencia debe ser positivo')
        return v

    @validator('preferred_modality')
    def preferred_modality_valid(cls, v):
        if v not in [1, 2, 3]:  # 1=Presencial, 2=Remoto, 3=Híbrido
            raise ValueError('La modalidad preferida debe ser 1, 2 o 3')
        return v

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
        required_fields = ['name', 'email', 'date_of_birth', 'location', 
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

@router.get("/register/student/example")
async def get_student_example():
    """Endpoint para mostrar un ejemplo del formato JSON esperado"""
    example = {
        "name": "Juan Pérez",
        "email": "juan.perez@example.com",
        "date_of_birth": "2000-01-15",
        "experience_id": 1,  # Opcional por ahora
        "location": "Lima, Perú",
        "weekly_availability": 20,
        "preferred_modality": 2,  # 1=Presencial, 2=Remoto, 3=Híbrido
        "career": "Ingeniería de Sistemas",
        "academic_cycle": 8,
        "main_motivation": "Ganar experiencia profesional",
        "description": "Estudiante de ingeniería con interés en desarrollo web y bases de datos"
    }
    return JSONResponse(content={
        "message": "Ejemplo de formato JSON para registrar estudiante",
        "example": example,
        "notes": {
            "preferred_modality": "1=Presencial, 2=Remoto, 3=Híbrido",
            "weekly_availability": "Horas por semana (1-40)",
            "academic_cycle": "Ciclo académico (1-12)",
            "experience_id": "ID de experiencia (opcional por ahora)"
        }
    })

@router.post("/register/student")
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