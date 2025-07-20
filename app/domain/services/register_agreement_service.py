from app.domain.entities.agreement import Agreement, AgreementStatus
from app.domain.repositories.agreement_repository import AgreementRepository
from app.application.ports.register_agreement_port import RegisterAgreementPort
from datetime import date

class RegisterAgreementService:
    def __init__(self, agreement_repo: AgreementRepository, register_agreement_port: RegisterAgreementPort):
        self.agreement_repo = agreement_repo
        self.register_agreement_port = register_agreement_port

    async def register_agreement(self, agreement_data: dict):
        # Validaciones de negocio básicas
        # Por ejemplo: verificar que el estudiante no tenga demasiados acuerdos activos
        # Verificar que la oferta de trabajo esté disponible
        # Verificar que el estudiante cumpla con los requisitos de la oferta
        
        # Crear entidad de dominio con constructor correcto
        agreement = Agreement(
            id=0,  # Se asignará automáticamente por la base de datos
            job_offer_id=agreement_data["job_offer_id"],
            student_id=agreement_data["student_id"],
            status=AgreementStatus.pending,
            start_date=agreement_data.get("start_date"),
            end_date=agreement_data.get("end_date")
        )
        
        # Guardar acuerdo usando el repositorio directamente
        saved_model = await self.agreement_repo.save(agreement)
        if saved_model:
            return saved_model.id  # Retornar solo el ID
        else:
            raise ValueError("Error al guardar el acuerdo")