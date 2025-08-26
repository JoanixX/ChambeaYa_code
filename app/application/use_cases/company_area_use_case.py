from app.application.ports.company_area_port import CompanyAreaPort
from app.domain.entities.company_area import CompanyArea
from app.domain.services.company_area_service import CompanyAreaService
from typing import Dict, Any, List

class CompanyAreaUseCase:
    def __init__(self, company_area_port: CompanyAreaPort, company_area_service: CompanyAreaService):
        self.company_area_port = company_area_port
        self.company_area_service = company_area_service

    async def get_company_areas(self, company_id: int) -> List[CompanyArea]:
        return await self.company_area_port.get_company_areas(company_id)

    async def add_company_area(self, company_area: CompanyArea) -> CompanyArea:
        area_id = await self.company_area_port.add_company_area(company_area) 

        if not area_id:
            raise ValueError("Error al agregar el area a la compañia")

        return area_id
    
    async def delete_company_area(self, company_id: int, area_id: int) -> Dict[str, Any]:
        success = await self.company_area_port.delete_company_area(company_id, area_id)

        if not success:
            raise ValueError(f"Error al eliminar el area con ID {area_id} de la compañia con ID {company_id}")

        return {
            "message": "Área eliminada exitosamente de la compañia"
        }