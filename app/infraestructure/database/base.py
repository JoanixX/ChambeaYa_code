from sqlalchemy.orm import declarative_base

#Este declarativa base sirve para que todas las entidades se puedan heredar y despues mapear bien
#si esto no se hace, es como si se creara un especie de mundo diferente por cada entidad y ninguna
#tiene relacion, entonces mejor se crea una base main por asi decirlo y todas las entidades heredan de esa base
Base = declarative_base()