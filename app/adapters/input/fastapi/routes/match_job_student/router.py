from .match_job_offer import router as match_job_offer_router
from .match_student import router as match_student_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(match_job_offer_router)
router.include_router(match_student_router)
