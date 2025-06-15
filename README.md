# ChambeaYA

ChambeaYA es una plataforma diseñada para conectar estudiantes universitarios con empresas a través de retos y proyectos reales, facilitando el desarrollo profesional y la colaboración entre ambos sectores. El sistema permite a las empresas registrar desafíos, y a los estudiantes postularse según sus intereses, habilidades y disponibilidad, generando matches inteligentes y acuerdos de colaboración.

---

## ¿De qué trata el proyecto?

El objetivo principal de ChambeaYA es crear un ecosistema donde:
- **Empresas** puedan publicar retos o proyectos reales, especificando sus necesidades, cultura y requerimientos.
- **Estudiantes** puedan registrarse, detallar su perfil académico y profesional, y postularse a los retos que mejor se adapten a sus intereses y habilidades.
- El sistema realice un proceso de matching inteligente, filtrando y recomendando las mejores combinaciones empresa-estudiante.
- Se gestionen acuerdos y el seguimiento de la experiencia.

La plataforma está pensada para ser escalable, mantenible y fácil de extender, permitiendo la integración de nuevas funcionalidades y adaptaciones a diferentes contextos educativos y empresariales.

---

## Arquitectura Hexagonal (Ports & Adapters)

ChambeaYA está construido siguiendo el patrón de **arquitectura hexagonal** (también conocido como Ports & Adapters), que busca separar claramente la lógica de negocio del resto de la aplicación (infraestructura, frameworks, interfaces de usuario, etc.).

### ¿Cómo está organizada?

- **Dominio:**
  - Contiene las entidades principales (por ejemplo, `Student`, `Company`, `Match`), reglas de negocio y servicios puros.
  - No depende de detalles técnicos ni de frameworks externos.

- **Aplicación:**
  - Orquesta los casos de uso (por ejemplo, registrar estudiante, crear match, asignar cursos).
  - Define los **puertos** (interfaces abstractas) que describen lo que la aplicación necesita del dominio o de la infraestructura.

- **Adapters (Adaptadores):**
  - Implementan los puertos definidos en la capa de aplicación.
  - Incluyen los controladores HTTP (FastAPI), repositorios de base de datos, y cualquier integración externa.

- **Infraestructura:**
  - Proporciona detalles concretos de tecnologías (por ejemplo, conexión a base de datos, frameworks, librerías externas).

### Beneficios de la arquitectura hexagonal
- Permite cambiar la tecnología de base de datos, framework web o cualquier integración externa sin afectar la lógica de negocio.
- Facilita las pruebas unitarias y de integración, ya que la lógica de negocio está desacoplada de los detalles técnicos.
- Hace que el sistema sea más mantenible y escalable a largo plazo.

---

## Estructura general del repositorio

- `app/domain/`: Entidades, repositorios y servicios del dominio.
- `app/application/`: Casos de uso y puertos (interfaces de aplicación).
- `app/adapters/`: Adaptadores de entrada (FastAPI) y salida (ORM, otros servicios).
- `app/infraestructure/`: Configuración y utilidades de infraestructura (base de datos, etc.).

---

## Endpoints y API

La API está construida con FastAPI y expone endpoints para registrar empresas, estudiantes, gestionar matches, acuerdos y más. Para detalles de cada endpoint, consulta la documentación interna de cada módulo en `app/adapters/input/fastapi/routes/`.

---

## Instalación y ejecución rápida

1. Clona el repositorio y entra a la carpeta del proyecto.
2. Crea y activa un entorno virtual de Python.
3. Instala las dependencias:
   ```sh
   pip install -r requirements.txt
   ```
4. Ejecuta la aplicación:
   ```sh
   uvicorn app.main:app --reload
   ```
5. Accede a la documentación interactiva en [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Contribuciones

Las contribuciones son bienvenidas. Por favor, revisa la estructura y la arquitectura antes de proponer cambios importantes.

---

## Créditos

Desarrollado por el equipo ChambeaYA.

---

# (Guía de instalación original)

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

===========================================================================

6) Instalar el fastAPI (pip install "fastapi[standard]")
7) verificar la instalación con (pip freeze)
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

Para entrar a la documentación realizada por defecto de fastAPI:
- http://127.0.0.1:8000/docs

Para entrar a la documentación alternativa realizada por defecto por fastAPI:
- http://127.0.0.1:8000/redoc