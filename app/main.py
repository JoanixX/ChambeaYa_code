from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from app.adapters.input.fastapi.routes.match_job_student.router import router as match_job_student_router
from app.adapters.input.fastapi.routes.filter_match.router import router as filter_match_router
from app.adapters.input.fastapi.routes.agreement import router as agreement_router
from app.adapters.input.fastapi.routes.app_user import router as app_user_router
from app.adapters.input.fastapi.routes.area import router as area_router
from app.adapters.input.fastapi.routes.chat_history import router as chat_history_router
from app.adapters.input.fastapi.routes.company_area import router as company_area_router
from app.adapters.input.fastapi.routes.company import router as company_router
from app.adapters.input.fastapi.routes.experience_detail import router as experience_detail_router
from app.adapters.input.fastapi.routes.external_link import router as external_link_router
from app.adapters.input.fastapi.routes.interest import router as interest_router
from app.adapters.input.fastapi.routes.job_offer_area import router as job_offer_area_router
from app.adapters.input.fastapi.routes.job_offer_required_skill import router as job_offer_required_skill_router
from app.adapters.input.fastapi.routes.job_offer import router as job_offer_router
from app.adapters.input.fastapi.routes.skill import router as skill_router
from app.adapters.input.fastapi.routes.student_interest import router as student_interest_router
from app.adapters.input.fastapi.routes.student_skill import router as student_skill_router
from app.adapters.input.fastapi.routes.student import router as student_router

from app.domain.entities.agreement import Agreement
from app.domain.entities.app_user import AppUser
from app.domain.entities.area import Area
from app.domain.entities.chat_history import ChatHistory
from app.domain.entities.company_area import CompanyArea
from app.domain.entities.company import Company
from app.domain.entities.experience_detail import ExperienceDetail
from app.domain.entities.external_link import ExternalLink
from app.domain.entities.filter_match import FilterMatch
from app.domain.entities.interest import Interest
from app.domain.entities.job_offer_area import JobOfferArea
from app.domain.entities.job_offer_required_skill import JobOfferRequiredSkill
from app.domain.entities.job_offer import JobOffer
from app.domain.entities.match_job_student import MatchJobStudent
from app.domain.entities.skill import Skill
from app.domain.entities.student_interest import StudentInterest
from app.domain.entities.student_skill import StudentSkill
from app.domain.entities.student import Student

# ...otros modelos...

app = FastAPI()

app.include_router(agreement_router, prefix= "/api")
app.include_router(app_user_router, prefix="/api")
app.include_router(area_router, prefix="/api")
app.include_router(chat_history_router, prefix="/api")
app.include_router(company_area_router, prefix="/api")
app.include_router(company_router, prefix= "/api")
app.include_router(experience_detail_router, prefix="/api")
app.include_router(external_link_router, prefix="/api")
app.include_router(filter_match_router, prefix="/api")
app.include_router(interest_router, prefix="/api")
app.include_router(job_offer_area_router, prefix="/api")
app.include_router(job_offer_required_skill_router, prefix="/api")
app.include_router(job_offer_router, prefix="/api")
app.include_router(match_job_student_router, prefix="/api")
app.include_router(skill_router, prefix="/api")
app.include_router(student_interest_router, prefix="/api")
app.include_router(student_skill_router, prefix="/api")
app.include_router(student_router, prefix = "/api")

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