from fastapi import FastAPI

app = FastAPI()

mypes = [
    {
        "id": 1,
        "name": "Google",
        "url": "https://www.google.com",
        "disponible": True
    },
    {
        "id": 2,
        "name": "Apple",
        "url": "https://www.apple.com",
        "disponible": False
    },
    {
        "id": 3,
        "name": "Amazon",
        "url": "https://www.amazon.com",
        "disponible": False
    },
    {
        "id": 4,
        "name": "Microsoft",
        "url": "https://www.microsoft.com",
        "disponible": True
    }
]


@app.get("/")
def index():
    return {
        "message": "prueba1"
    }

#Listar todas las mypes
@app.get("/mypes")
def get_mypes():
    return {
        "mypes" : mypes
    }

#Obtener una mype por su id
@app.get("/mypes/{mype_id}")
def get_mype_by_id(mype_id: int):
    for m in mypes:
        if m["id"] == mype_id:
            return {
                "mype": m
            }
    return {
        "message": "Mype no encontrada"
    }

