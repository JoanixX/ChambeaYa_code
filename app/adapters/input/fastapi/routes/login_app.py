from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.infraestructure.database.connection import get_session
from app.domain.entities.app_user import AppUser, UserRole
from app.domain.entities.company import Company
from app.domain.entities.student import Student
from pydantic import BaseModel, EmailStr
from .jwt_utils import create_access_token, verify_password

router = APIRouter()

class LoginInput(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
async def login(credentials: LoginInput, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(AppUser).where(AppUser.email == credentials.email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    extra = {}
    if user.role == UserRole.company:
        company = await session.get(Company, user.related_id)
        if company:
            extra = {"company_id": company.id, "company_name": company.name}
    elif user.role == UserRole.student:
        student = await session.get(Student, user.related_id)
        if student:
            extra = {"student_id": student.id, "student_name": student.name}
    access_token = create_access_token({"sub": user.email, "role": user.role.value})
    return {"access_token": access_token, "token_type": "bearer", "role": user.role.value, **extra}