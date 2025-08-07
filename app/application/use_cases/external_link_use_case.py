from typing import Optional, List, Dict, Any

from app.application.ports.external_link_port import ExternalLinkPort
from app.domain.services.external_link_service import ExternalLinkService
from app.adapters.input.fastapi.schemas.external_link_schema import ExternalLinkResponse

class ExternalLinkUseCase:
    def __init__(self, external_link_port: ExternalLinkPort, external_link_service: ExternalLinkService):
        self.external_link_port = external_link_port
        self.external_link_service = external_link_service

    async def register_external_link(self, link_data: Dict[str, Any]) -> int:
        link_id = await self.external_link_service.register_external_link(link_data)

        if not link_id:
            raise ValueError("Error al guardar el enlace externo")

        return link_id

    async def get_all_external_links(self) -> List[ExternalLinkResponse]:
        links = await self.external_link_port.get_all_external_links()
        return [ExternalLinkResponse(id=l.id, url=l.url) for l in links]
    
    async def get_external_link(self, link_id: int) -> ExternalLinkResponse:
        link = await self.external_link_port.get_external_link(link_id)
        if not link:
            raise ValueError(f"Enlace externo con ID {link_id} no encontrado")
        return ExternalLinkResponse(id=link.id, url=link.url)
    
    async def delete_external_link(self, link_id: int) -> Dict[str, Any]:
        link = await self.external_link_port.get_external_link(link_id)
        if not link:
            raise ValueError(f"Enlace externo con ID {link_id} no encontrado")

        success = await self.external_link_port.delete_external_link(link_id)
        if not success:
            raise ValueError(f"Error al eliminar enlace externo con ID {link_id}")

        return {
            "message": "Enlace externo eliminado exitosamente"
        }
    
    async def get_external_link_url_by_id(self, link_id: int) -> Optional[str]:
        link_url = await self.external_link_port.get_external_link_url_by_id(link_id)
        if not link_url:
            raise ValueError(f"Enlace externo con ID {link_id} no encontrado")
        return link_url