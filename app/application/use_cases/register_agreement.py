from app.application.ports.register_agreement_port import RegisterAgreementPort
from app.domain.entities.agreement import Agreement, AgreementStatus
from app.domain.services.agreement_policy_checker import AgreementPolicyChecker

class RegisterAgreementUseCase:
    def __init__(self, register_agreement_port: RegisterAgreementPort, policy_checker: AgreementPolicyChecker):
        self.register_agreement_port = register_agreement_port
        self.policy_checker = policy_checker

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
        
        # Verificar políticas de negocio
        if not await self.policy_checker.validate_agreement_policies(agreement_data):
            raise ValueError("El acuerdo no cumple con las políticas de la empresa")
        
        # Crear entidad de dominio
        agreement = Agreement(
            job_offer_id=agreement_data["job_offer_id"],
            student_id=agreement_data["student_id"],
            status=AgreementStatus.pending,
            start_date=agreement_data.get("start_date"),
            end_date=agreement_data.get("end_date")
        )
        
        # Registrar acuerdo
        saved_agreement = await self.register_agreement_port.register_agreement(agreement)
        
        return {
            "agreement_id": saved_agreement.id,
            "registration_success": True,
            "status": saved_agreement.status.value
        }
