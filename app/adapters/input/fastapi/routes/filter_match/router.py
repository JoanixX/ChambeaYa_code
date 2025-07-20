from .filter_job_offer import router as filter_job_offer_router
from .filter_student import router as filter_student_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(filter_job_offer_router)
router.include_router(filter_student_router)
