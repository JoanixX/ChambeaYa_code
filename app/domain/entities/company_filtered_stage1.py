from fastapi import APIRouter, Body
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse

router = APIRouter()

class CompanyProfileInput(BaseModel):
    profile_text: str = Field(..., description="Texto completo del perfil de la empresa para vectorización")

@router.post("/profile/vectorize/company/test")
async def test_vectorize_company_profile(payload: CompanyProfileInput = Body(...)):
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform([payload.profile_text])
        vector = X.toarray()[0].tolist()
        feature_names = vectorizer.get_feature_names_out()
        return JSONResponse(content={
            "message": "Test exitoso de vectorización TF-IDF",
            "vector": vector,
            "features": feature_names.tolist(),
            "profile_text": payload.profile_text
        })
    except ImportError as e:
        import sys
        return JSONResponse(content={
            "error": "scikit-learn no está instalado",
            "sys_path": sys.path,
            "python_executable": sys.executable,
            "exception": str(e)
        }, status_code=500)
    except Exception as e:
        import traceback
        return JSONResponse(content={
            "error": "Error inesperado en la vectorización",
            "exception": str(e),
            "traceback": traceback.format_exc()
        }, status_code=500)

