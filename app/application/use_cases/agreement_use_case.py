from app.application.ports.agreement_port import AgreementPort
from app.domain.services.agreement_service import AgreementService
from app.domain.entities.agreement import Agreement
from typing import Dict, Any, List

class AgreementUseCase:
    def __init__(self, agreement_port: AgreementPort, agreement_service: AgreementService):
        self.agreement_port = agreement_port
        self.agreement_service = agreement_service

    async def register_agreement(self, agreement_data: Dict[str, Any]) -> Dict[str, Any]:
        if not await self.agreement_port.validate_agreement_data(agreement_data):
            raise ValueError("Datos de acuerdo inválidos")

        if await self.agreement_port.check_agreement_exists(
            agreement_data["student_id"],
            agreement_data["job_offer_id"]
        ):
            raise ValueError("Ya existe un acuerdo entre este estudiante y oferta de trabajo")

        agreement_id = await self.agreement_service.register_agreement(agreement_data)

        if not agreement_id:
            raise ValueError("Error al guardar el acuerdo")
        
        return {
            "agreement_id": agreement_id,
            "registration_success": True,
            "message": "Acuerdo registrado exitosamente"
        }
    
    async def get_agreement(self, agreement_id: int) -> Agreement:
        agreement = await self.agreement_port.get_agreement(agreement_id)
        if not agreement:
            raise ValueError(f"Acuerdo con ID {agreement_id} no encontrado")
        return agreement

    async def get_student_agreements(self, student_id: int) -> List[Agreement]:
        agreements = await self.agreement_port.get_student_agreements(student_id)
        if not agreements:
            raise ValueError(f"No se encontraron acuerdos para el estudiante con ID {student_id}")
        return agreements

    async def get_job_offer_agreements(self, job_offer_id: int) -> List[Agreement]:
        agreements = await self.agreement_port.get_job_offer_agreements(job_offer_id)
        if not agreements:
            raise ValueError(f"No se encontraron acuerdos para la oferta de trabajo con ID {job_offer_id}")
        return agreements

    async def get_all_agreements(self) -> List[Agreement]:
        return await self.agreement_port.get_all_agreements()

    async def update_agreement(self, agreement_id: int, agreement_data: Dict[str, Any]) -> Agreement:
        if not await self.agreement_port.validate_agreement_data(agreement_data):
            raise ValueError("Datos de acuerdo inválidos")

        agreement = await self.agreement_port.get_agreement(agreement_id)
        if not agreement:
            raise ValueError(f"Acuerdo con ID {agreement_id} no encontrado")

        updated_agreement = await self.agreement_port.update_agreement(agreement_id, agreement_data)
        if not updated_agreement:
            raise ValueError(f"Error al actualizar acuerdo con ID {agreement_id}")

        return updated_agreement

    async def delete_agreement(self, agreement_id: int) -> Dict[str, Any]:
        agreement = await self.agreement_port.get_agreement(agreement_id)
        if not agreement:
            raise ValueError(f"Acuerdo con ID {agreement_id} no encontrado")

        success = await self.agreement_port.delete_agreement(agreement_id)
        if not success:
            raise ValueError(f"Error al eliminar acuerdo con ID {agreement_id}")

        return {
            "message": "Acuerdo eliminado exitosamente"
        }