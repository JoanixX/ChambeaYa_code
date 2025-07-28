from app.application.ports.agreement_port import AgreementPort
from app.domain.entities.agreement import Agreement, AgreementStatus
from app.domain.services.agreement_service import AgreementService
from datetime import date

class AgreementUseCase:
    def __init__(self, register_agreement_port: AgreementPort, register_agreement_service: AgreementService):
        self.register_agreement_port = register_agreement_port
        self.register_agreement_service = register_agreement_service

    async def execute(self, agreement_data: dict) -> dict:
        # Validar datos
        if not await self.register_agreement_port.validate_agreement_data(agreement_data):
            raise ValueError("Datos de acuerdo inválidos")
        
        # Verificar que no exista un acuerdo previo
        if await self.register_agreement_port.check_agreement_exists(
            agreement_data["student_id"], 
            agreement_data["job_offer_id"]
        ):
            raise ValueError("Ya existe un acuerdo entre este estudiante y oferta de trabajo")
        
        # Registrar acuerdo usando el servicio de dominio
        agreement_id = await self.register_agreement_service.register_agreement(agreement_data)
        
        # Verificar que el acuerdo se guardó correctamente
        if not agreement_id:
            raise ValueError("Error al guardar el acuerdo")
        
        return {
            "agreement_id": agreement_id,
            "registration_success": True,
            "status": "pending",
            "message": "Acuerdo registrado exitosamente"
        }