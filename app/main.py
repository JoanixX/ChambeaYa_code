from fastapi import FastAPI
from app.adapters.input.fastapi.routes.student import router as student_router, StudentCreate
from app.adapters.input.fastapi.routes.company import router as company_router, CompanyCreate
from datetime import date, datetime
from fastapi.responses import JSONResponse

app = FastAPI()

# Incluir routers
app.include_router(student_router)
app.include_router(company_router)

@app.get("/")
def read_root():
    return {"message": "holaaaaaAaAAA a la api"}

@app.get("/test-validation")
def test_validation():
    try:
        valid_student = StudentCreate(
            name="Juan Perez",
            email="juan.perez@email.com",
            date_of_birth=date(2000, 5, 10),
            enrollment_date=datetime(2024, 6, 1, 10, 0, 0)
        )
        valid_student_result = "OK"
    except Exception as e:
        valid_student_result = str(e)
    try:
        invalid_student = StudentCreate(
            name=" ",
            email="noesunemail",
            date_of_birth=date(2030, 1, 1),
            enrollment_date=datetime(2030, 1, 1, 10, 0, 0)
        )
        invalid_student_result = "OK"
    except Exception as e:
        invalid_student_result = str(e)

    try:
        valid_company = CompanyCreate(
            name="Empresa Ejemplo",
            industry="Tecnología",
            contact_name="Ana López",
            email="empresa@ejemplo.com"
        )
        valid_company_result = "OK"
    except Exception as e:
        valid_company_result = str(e)
    try:
        invalid_company = CompanyCreate(
            name="",
            industry=" ",
            contact_name="",
            email="noesunemail"
        )
        invalid_company_result = "OK"
    except Exception as e:
        invalid_company_result = str(e)

    return JSONResponse({
        "message": "Validaciones de prueba",
        "valid_student": valid_student_result,
        "invalid_student": invalid_student_result,
        "valid_company": valid_company_result,
        "invalid_company": invalid_company_result
    })