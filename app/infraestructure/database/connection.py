import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from typing import AsyncGenerator
from sqlalchemy.orm import sessionmaker

#la cadena de conexión se lee del entorno, nunca se versiona en el repositorio.
#ejemplo: postgresql+asyncpg://usuario:clave@host:5432/chambeaya-bd?ssl=require
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "Falta la variable de entorno DATABASE_URL. "
        "Definirla con la cadena de conexión asyncpg de PostgreSQL, por ejemplo: "
        "postgresql+asyncpg://usuario:clave@host:5432/chambeaya-bd?ssl=require"
    )

#el echo vuelca cada sentencia SQL con sus parámetros, así que solo se activa
#bajo demanda (SQL_ECHO=true) y queda apagado en producción.
SQL_ECHO = os.getenv("SQL_ECHO", "false").lower() == "true"

#creamos el engine asíncrono
engine = create_async_engine(
    DATABASE_URL,
    echo=SQL_ECHO
)

#creamos una sesión asincrona para interactue con la base de datos
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

#dependencia para obtener la sesion asincrona
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
