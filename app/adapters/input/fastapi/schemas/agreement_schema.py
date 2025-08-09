from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date
from app.adapters.input.fastapi.validators import not_empty, start_date_future, positive_int
from app.domain.entities.agreement import AgreementStatus

class AgreementCreate(BaseModel):
    job_offer_id: int = Field(..., description="ID de la oferta de trabajo")
    student_id: int = Field(..., description="ID del estudiante")
    start_date: Optional[date] = Field(None, description="Fecha de inicio")
    end_date: Optional[date] = Field(None, description="Fecha de fin")
    status: Optional[AgreementStatus] = Field(default=AgreementStatus.pending, description="Estado del acuerdo")

    @field_validator('job_offer_id', 'student_id', 'start_date', 'end_date')
    def not_empty(cls, v, info):
        return not_empty(v, info.field_name)

    @field_validator('job_offer_id')
    def job_offer_id_positive(cls, v, info):
        return positive_int(v, 'El ID de la oferta de trabajo debe ser positivo')
    
    @field_validator('student_id')
    def student_id_positive(cls, v, info):
        return positive_int(v, 'El ID del estudiante debe ser positivo')

    @field_validator('start_date')
    def start_date_not_in_future(cls, v, info):
        return start_date_future(v, 'La fecha de inicio no puede ser en el pasado')

    @field_validator('end_date')
    def end_date_after_start(cls, v, info):
        start_date = info.data.get('start_date') if info.data else None
        if v and start_date:
            if v <= start_date:
                raise ValueError('La fecha de fin debe ser posterior a la fecha de inicio')
        return v

class AgreementResponse(BaseModel):
    id: int
    job_offer_id: int
    student_id: int
    start_date: Optional[date]
    end_date: Optional[date]
    status: AgreementStatus