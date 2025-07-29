import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from app.adapters.input.fastapi.routes.student import router as student_router, StudentCreate
from app.adapters.input.fastapi.routes.company import router as company_router, CompanyCreate
from app.adapters.input.fastapi.routes.login_app import router as login_router
from app.adapters.input.fastapi.routes.register_app import router as register_router
from app.adapters.input.fastapi.routes.agreement import router as agreement_router
from fastapi.middleware.cors import CORSMiddleware
from app.adapters.input.fastapi.routes.match_job_student.router import router as match_job_student_router
from app.adapters.input.fastapi.routes.filter_match.router import router as filter_match_router
from app.adapters.input.fastapi.routes.job_offer import router as job_offer_router
from app.adapters.input.fastapi.routes.job_offer_required_skill import router as job_offer_required_skill_router
from app.adapters.input.fastapi.routes.skill import router as skill_router

from app.domain.entities.experience_detail import ExperienceDetail
from app.domain.entities.student import Student
from app.domain.entities.company import Company
from app.domain.entities.area import Area
from app.domain.entities.job_offer import JobOffer
from app.domain.entities.agreement import Agreement
from app.domain.entities.match_job_student import MatchJobStudent
from app.domain.entities.filter_match import FilterMatch
from app.domain.entities.job_offer_required_skill import JobOfferRequiredSkill
from app.domain.entities.external_link import ExternalLink
from app.domain.entities.skill import Skill
from app.domain.entities.student_skill import StudentSkill
from app.domain.entities.student_interest import StudentInterest
from app.domain.entities.interest import Interest
# ...otros modelos...

app = FastAPI()

app.include_router(student_router, prefix = "/api")
app.include_router(company_router, prefix= "/api")
app.include_router(agreement_router, prefix= "/api")
app.include_router(match_job_student_router, prefix="/api")
app.include_router(filter_match_router, prefix="/api")
app.include_router(login_router, prefix="/api")
app.include_router(register_router, prefix="/api")
app.include_router(job_offer_router, prefix="/api")
app.include_router(job_offer_required_skill_router, prefix="/api")
app.include_router(skill_router, prefix="/api") 

#configuracion para el cors
origins = [
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    "http://localhost:8001",
    "http://127.0.0.1:8001",
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