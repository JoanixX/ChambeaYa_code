from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from typing import AsyncGenerator
from sqlalchemy.orm import sessionmaker

#conexion a la base de datos PostgreSQL
## DATABASE_URL = "postgresql+asyncpg://postgres:etc100charmander@localhost:5432/chambeaya-db"
DATABASE_URL = "postgresql+asyncpg://admindbchambeaya%40db-postgresql-chambeaya:1qa.!QA.@db-postgresql-chambeaya.postgres.database.azure.com:5432/chambeaya-db?ssl=require"


#creamos el engine asíncrono
engine = create_async_engine(
    DATABASE_URL,
    echo=True  #el echo hace que se muestren las consultas en consola
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
