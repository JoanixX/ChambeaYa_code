from app.application.ports.company_port import CompanyPort
from app.domain.entities.company import Company
from app.domain.services.company_service import CompanyService
from typing import Dict, Any, List

class CompanyUseCase:
    def __init__(self, company_port: CompanyPort, company_service: CompanyService):
        self.company_port = company_port
        self.company_service = company_service

    async def register_company(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        if not await self.company_port.validate_company_data(company_data):
            raise ValueError("Datos de la empresa inválidos")

        company_id = await self.company_service.register_company(company_data)

        if not company_id:
            raise ValueError("Error al guardar la empresa")

        return {
            "company_id": company_id,
            "registration_success": True,
            "message": "Empresa registrada exitosamente"
        }
    
    async def get_company(self, company_id: int) -> Company:
        company = await self.company_port.get_company(company_id)
        if not company:
            raise ValueError(f"Empresa con ID {company_id} no encontrada")
        return company
    
    async def get_all_companies(self) -> List[Company]:
        return await self.company_port.get_all_companies()
    
    async def update_company(self, company_id: int, company_data: Dict[str, Any]) -> Company:
        if not await self.company_port.validate_company_data(company_data):
            raise ValueError("Datos de la empresa inválidos")

        company = await self.company_port.get_company(company_id)
        if not company:
            raise ValueError(f"Empresa con ID {company_id} no encontrada")

        updated_company = await self.company_port.update_company(company_id, company_data)
        if not updated_company:
            raise ValueError(f"Error al actualizar empresa con ID {company_id}")

        return updated_company
    
    async def delete_company(self, company_id: int) -> Dict[str, Any]:
        company = await self.company_port.get_company(company_id)
        if not company:
            raise ValueError(f"Empresa con ID {company_id} no encontrada")

        success = await self.company_port.delete_company(company_id)
        if not success:
            raise ValueError(f"Error al eliminar empresa con ID {company_id}")

        return {
            "message": "Empresa eliminada exitosamente"
        }