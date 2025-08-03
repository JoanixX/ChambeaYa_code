from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.connection import get_session
from app.application.factories.app_user_factory import AppUserUseCaseFactory
from app.adapters.input.fastapi.schemas.app_user_schema import AppUserCreate, AppUserResponse

router = APIRouter()

@router.post("/register/user", response_model=AppUserResponse)
async def register_user(user: AppUserCreate, session: AsyncSession = Depends(get_session)):
    try:
        user_use_case = AppUserUseCaseFactory(session).build()
        new_user = await user_use_case.register_user(
            email=user.email,
            password=user.password,
            role=user.role,
            related_id=user.related_id
        )
        return AppUserResponse(
            id=new_user.id,
            email=new_user.email,
            role=new_user.role,
            related_id=new_user.related_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")