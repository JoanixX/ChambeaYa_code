from app.application.ports.register_company_port import RegisterCompanyPort
from app.domain.entities.company import Company
from app.domain.services.register_company_service import RegisterCompanyService

class RegisterCompanyUseCase:
    def __init__(self, register_company_port: RegisterCompanyPort, register_company_service: RegisterCompanyService):
        self.register_company_port = register_company_port
        self.register_company_service = register_company_service

    async def execute(self, company_data: dict) -> dict:
        # Validar datos
        if not await self.register_company_port.validate_company_data(company_data):
            raise ValueError("Datos de empresa inválidos")
        
        # Verificar RUC único
        if await self.register_company_port.check_ruc_exists(company_data["RUC"]):
            raise ValueError("El RUC ya está registrado")
        
        # Verificar email único
        if await self.register_company_port.check_email_exists(company_data["email"]):
            raise ValueError("El email ya está registrado")
        
        # Registrar empresa usando el servicio de dominio
        company_id = await self.register_company_service.register_company(company_data)
        
        # Verificar que la empresa se guardó correctamente
        if not company_id:
            raise ValueError("Error al guardar la empresa")
        
        return {
            "company_id": company_id,
            "registration_success": True,
            "message": "Empresa registrada exitosamente"
        }