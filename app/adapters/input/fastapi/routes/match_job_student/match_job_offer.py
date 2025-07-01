from fastapi import APIRouter, Body

router = APIRouter()

@router.post("/aimodel/job_offer/matching_offers")
def matching_offers(data: dict = Body(...)):
    # Simulación de matching
    score = 0.85  # Reemplazar por lógica real
    return {"score": score, "details": data}
