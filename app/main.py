from fastapi import FastAPI
from app.adapters.input.fastapi.routes.student import router as student_router, StudentCreate
from app.adapters.input.fastapi.routes.company import router as company_router, CompanyCreate
from app.adapters.input.fastapi.routes.match import router as match_router
from app.adapters.input.fastapi.routes.filter_match import router as filter_match_router
from app.adapters.input.fastapi.routes.login_app import router as login_router
from app.adapters.input.fastapi.routes.register_app import router as register_router
from fastapi.middleware.cors import CORSMiddleware
from datetime import date, datetime
from fastapi.responses import JSONResponse

# --- IMPORTS DE TODOS LOS MODELOS PARA REGISTRAR EL METADATA ---
from app.domain.entities.experience_detail import ExperienceDetail
from app.domain.entities.student import Student
from app.domain.entities.company import Company
from app.domain.entities.agreement import Agreement
from app.domain.entities.area import Area
from app.domain.entities.app_user import AppUser
from app.domain.entities.external_link import ExternalLink
from app.domain.entities.filter_match import FilterMatch
from app.domain.entities.interest import Interest
from app.domain.entities.job_offer import JobOffer
from app.domain.entities.job_offer_required_skill import JobOfferRequiredSkill
from app.domain.entities.match_job_student import MatchJobStudent
from app.domain.entities.skill import Skill
from app.domain.entities.student_interest import StudentInterest
from app.domain.entities.student_skill import StudentSkill

app = FastAPI()

# Incluir routers
app.include_router(student_router)
app.include_router(company_router)
app.include_router(match_router)
app.include_router(filter_match_router)
app.include_router(login_router)
app.include_router(register_router)

# Configuracion para el cors
origins = [
    "http://localhost:5000",
    "http://127.0.0.1:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "holaaaaaAaAAA a la api"}

@app.get("/test-validation")
def test_validation():
    results = {}
    # Prueba estudiante válido
    try:
        valid_student = StudentCreate(
            name="Juan Perez",
            email="juan.perez@email.com",
            date_of_birth=date(2000, 5, 10),
            experience_id=1,
            enrollment_date=datetime(2024, 6, 1, 10, 0, 0),
            location="Lima",
            star_skill_id=2,
            main_motivation_id=3,
            weekly_availability=20,
            preferred_modality_id=1,
            career="Ingeniería",
            academic_cycle=5
        )
        results['valid_student'] = "OK"
    except Exception as e:
        results['valid_student'] = str(e)
    # Prueba estudiante inválido
    try:
        invalid_student = StudentCreate(
            name=" ",
            email="noesunemail",
            date_of_birth=date(2030, 1, 1),
            experience_id=None,
            enrollment_date=datetime(2030, 1, 1, 10, 0, 0),
            location=" ",
            star_skill_id=None,
            main_motivation_id=None,
            weekly_availability=None,
            preferred_modality_id=None,
            career=" ",
            academic_cycle=None
        )
        results['invalid_student'] = "OK"
    except Exception as e:
        results['invalid_student'] = str(e)
    #prueba una compañia valida
    try:
        valid_company = CompanyCreate(
            name="Empresa Ejemplo",
            tax_id="123456789",
            industry="Tecnología",
            challenge_area_id=1,
            challenge_description="Desafío de ejemplo",
            company_culture="Innovadora",
            required_hours=40,
            project_modality_id=2,
            contact_name="Ana López",
            email="empresa@ejemplo.com"
        )
        results['valid_company'] = "OK"
    except Exception as e:
        results['valid_company'] = str(e)
    #prueba la compañia invalida
    try:
        invalid_company = CompanyCreate(
            name="",
            tax_id="",
            industry=" ",
            challenge_area_id=None,
            challenge_description=None,
            company_culture="",
            required_hours=None,
            project_modality_id=None,
            contact_name="",
            email="noesunemail"
        )
        results['invalid_company'] = "OK"
    except Exception as e:
        results['invalid_company'] = str(e)
    return JSONResponse(content=results)