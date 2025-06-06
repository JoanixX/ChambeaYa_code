Versión de pip usada: 25.1.1

Pasos para configurar el entorno local con fastAPI:
1) Crear una carpeta
2) Entrar a la carpeta desde la terminal
3) Abrir el VSCode desde la carpeta
4) Crear un entorno virtual con Python (py -m venv venv)

===========================================================================
Para Windows:
5) Una vez creado, entrar al venv desde la terminal 
(venv\Scripts\Activate.ps1 -> en PowerShell)
(venv\Scripts\actívate.bat -> en cmd.exe)

Para Linux:
5) Entrar al venv desde la terminal
(venv/bin/actívate -> bash/zsh)
(venv/bin/activate.fish -> fish)
(venv/bin/activate.csh -> csh/tcsh)
(venv/bin/Activate.ps1 -> pwsh)

Para MacOS:
5) 
===========================================================================

6) Instalar el fastAPI (pip install "fastapi[standard]")
7) verificar la instalación con (pip freeze), debe salir algo como esto:
annotated-types==0.7.0
anyio==4.9.0
certifi==2025.4.26
click==8.2.1
colorama==0.4.6
dnspython==2.7.0
email_validator==2.2.0
fastapi==0.115.12
fastapi-cli==0.0.7
h11==0.16.0
httpcore==1.0.9
httptools==0.6.4
httpx==0.28.1
idna==3.10
Jinja2==3.1.6
markdown-it-py==3.0.0
MarkupSafe==3.0.2
mdurl==0.1.2
pydantic==2.11.5
pydantic_core==2.33.2
Pygments==2.19.1
python-dotenv==1.1.0
python-multipart==0.0.20
PyYAML==6.0.2
rich==14.0.0
rich-toolkit==0.14.7
shellingham==1.5.4
sniffio==1.3.1
starlette==0.46.2
typer==0.16.0
typing-inspection==0.4.1
typing_extensions==4.14.0
uvicorn==0.34.3
watchfiles==1.0.5
websockets==15.0.1
8) En el VSC, creamos un archivo main.py donde pondremos un script de prueba
9) Ponemos cualquier tipo de script de prueba (
from fastapi import FastAPI

app = FastAPI()
@app.get("/")

def index():
    return {
        "message": "prueba1"
    }
)
10) Volvemos a la terminal y ejecutamos el archivo para comprobar si funciona (uvicorn main:app --reload)
11) Ingresamos a la ruta que da el unicorn y verificamos si se muestra el mensaje

==========================================================================================================
Para entrar a la documentación realizada por defecto de fastAPI:
- http://127.0.0.1:8000/docs

Para entrar a la documentación alternativa realizada por defecto por fastAPI:
- http://127.0.0.1:8000/redoc
==========================================================================================================