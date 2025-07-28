from pydantic import BaseModel, Field, EmailStr
from app.adapters.input.fastapi.validators import not_empty, not_in_future, in_range, positive_int, in_choices
from datetime import date
from typing import Optional,Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session
from app.application.use_cases.student_use_case import StudentUseCase
from app.adapters.output.orm.repositories.student_repository_impl import StudentRepositoryImpl
from app.domain.services.student_service import StudentService
from app.application.ports.student_port import StudentPort
from app.domain.entities.student import Student
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
    
    @field_validator('email')
    def valid_email(cls, v):
        return EmailStr._validate(v)

router = APIRouter()

class StudentPortImpl(StudentPort):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.student_repo = StudentRepositoryImpl(session)

    async def register_student(self, student_data: Dict[str, Any]) -> Student:
        student = Student(
            id=0,
            name=student_data["name"],
            email=student_data["email"],
            career=student_data["career"],
            academic_cycle=student_data["academic_cycle"],
            location=student_data["location"],
            main_motivation=student_data["main_motivation"],
            description=student_data["description"],
            weekly_availability=student_data["weekly_availability"],
            preferred_modality=student_data["preferred_modality"],
            experience_id=student_data.get("experience_id", None),
            date_of_birth=student_data["date_of_birth"],
            embedding={}
        )

        # Guardar estudiante
        saved_student = await self.student_repo.save(student)
        return saved_student

    async def get_student(self, student_id: int) -> Optional[Student]:
        return await self.student_repo.find_by_id(student_id)

    async def get_all_students(self) -> list[Student]:
        return await self.student_repo.get_all()

    async def update_student(self, student_id: int, student_data: Dict[str, Any]) -> Optional[Student]:
        existing_student = await self.student_repo.find_by_id(student_id)
        if not existing_student:
            return None

        updated_student = Student(
            id=student_id,
            name=student_data.get("name", existing_student.name),
            email=student_data.get("email", existing_student.email),
            career=student_data.get("career", existing_student.career),
            academic_cycle=student_data.get("academic_cycle", existing_student.academic_cycle),
            location=student_data.get("location", existing_student.location),
            main_motivation=student_data.get("main_motivation", existing_student.main_motivation),
            description=student_data.get("description", existing_student.description),
            weekly_availability=student_data.get("weekly_availability", existing_student.weekly_availability),
            preferred_modality=student_data.get("preferred_modality", existing_student.preferred_modality),
            experience_id=student_data.get("experience_id", existing_student.experience_id),
            date_of_birth=student_data.get("date_of_birth", existing_student.date_of_birth),
            embedding=student_data.get("embedding", existing_student.embedding)
        )

        return await self.student_repo.update(updated_student)

    async def delete_student(self, student_id: int) -> bool:
        return await self.student_repo.delete(student_id)

    async def validate_student_data(self, student_data: Dict[str, Any]) -> bool:
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

@router.post("/register/student", response_model=dict, tags=["Estudiante"])
async def register_student(request: Request, student: StudentCreate, session: AsyncSession = Depends(get_session)):
    try:
        body = await request.body()
        logger.info(f"Body recibido: {body.decode()}")
        logger.info(f"Iniciando registro de estudiante: {student.email}")
        
        student_port = StudentPortImpl(session)
        student_repo = StudentRepositoryImpl(session)
        student_service = StudentService(student_repo)

        use_case = StudentUseCase(student_port, student_service)

        logger.info("Ejecutando caso de uso...")
        result = await use_case.register_student(student.dict())
        
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
    try:
        student_port = StudentPortImpl(session)
        student_repo = StudentRepositoryImpl(session)
        student_service = StudentService(student_repo)
        use_case = StudentUseCase(student_port, student_service)
        student = await use_case.get_student(student_id)

        return student.__dict__
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.get("/student/all", response_model=list, tags=["Estudiante"])
async def get_all_students(session: AsyncSession = Depends(get_session)):
    try:
        student_port = StudentPortImpl(session)
        student_repo = StudentRepositoryImpl(session)
        student_service = StudentService(student_repo)
        use_case = StudentUseCase(student_port, student_service)
        students = await use_case.get_all_students()

        return [s.__dict__ for s in students]
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.put("/student/{student_id}", response_model=dict, tags=["Estudiante"])
async def update_student(student_id: int, student: StudentCreate, session: AsyncSession = Depends(get_session)):
    try:
        student_port = StudentPortImpl(session)
        student_repo = StudentRepositoryImpl(session)
        student_service = StudentService(student_repo)
        use_case = StudentUseCase(student_port, student_service)
        updated_student = await use_case.update_student(student_id, student.dict())

        return updated_student.__dict__
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@router.delete("/student/{student_id}", response_model=dict, tags=["Estudiante"])
async def delete_student(student_id: int, session: AsyncSession = Depends(get_session)):
    try:
        student_port = StudentPortImpl(session)
        student_repo = StudentRepositoryImpl(session)
        student_service = StudentService(student_repo)
        use_case = StudentUseCase(student_port, student_service)
        result = await use_case.delete_student(student_id)

        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")