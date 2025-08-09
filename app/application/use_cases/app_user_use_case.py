from app.domain.entities.app_user import AppUser
from app.domain.services.app_user_service import AppUserService
from app.application.ports.app_user_port import AppUserPort
from app.adapters.output.orm.models.student_model import StudentModel
from app.adapters.output.orm.models.company_model import CompanyModel

from typing import Dict, Any
from app.core.security.jwt_utils import create_access_token
from app.core.security.jwt_utils import get_password_hash

class AppUserUseCase:
    def __init__(self, user_port: AppUserPort, service: AppUserService):
        self.user_port = user_port
        self.user_service = service

    async def get_user_by_email(self, email: str) -> AppUser:
        user = await self.user_port.get_by_email(email)
        if not user:
            raise ValueError("Usuario no encontrado")
        return user

    async def register_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        if await self.user_port.get_by_email(user_data["email"]):
            raise ValueError("El email ya está registrado")
        
        if "password" in user_data:
            user_data["password_hash"] = get_password_hash(user_data.pop("password"))
        elif "password_hash" not in user_data:
            raise ValueError("Se requiere el campo password")

        user_id = await self.user_service.register_user(user_data)

        if not user_id:
            raise ValueError("Error al guardar el Usuario")

        return {
            "user_id": user_id,
            "registration_success": True,
            "message": "Usuario registrado exitosamente"
        }
    
    async def login(self, email: str, password: str, session) -> dict:
        user = await self.user_service.authenticate(email, password, session)
        if not user:
            raise ValueError("Credenciales incorrectas")
        extra = {}

        if hasattr(user, 'role'):
            role_value = user.role.value if hasattr(user.role, 'value') else user.role
            if role_value == "company":
                company = await session.get(CompanyModel, user.related_id)
                if company:
                    extra = {"company_id": company.id, "company_name": company.name}
            elif role_value == "student":
                student = await session.get(StudentModel, user.related_id)
                if student:
                    extra = {"student_id": student.id, "student_name": student.name}

        access_token = create_access_token({"sub": user.email, "role": role_value})
        return {"access_token": access_token, "token_type": "bearer", "role": role_value, **extra}