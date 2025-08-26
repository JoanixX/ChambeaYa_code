from typing import Dict, Any, List

from app.domain.entities.external_link import ExternalLink
from app.application.ports.external_link_port import ExternalLinkPort
from app.domain.services.external_link_service import ExternalLinkService

class ExternalLinkUseCase:
    def __init__(self, external_link_port: ExternalLinkPort, external_link_service: ExternalLinkService):
        self.external_link_port = external_link_port
        self.external_link_service = external_link_service

    async def register_external_link(self, external_link_data: Dict[str, Any]) -> Dict[str, Any]:
        external_link_id = await self.external_link_service.register_external_link(external_link_data)
        
        if not external_link_id:
            raise ValueError("Error al guardar link")

        return {
            "id": external_link_id,
            "registration_success": True,
            "message": "Link registrado exitosamente"
        }

    async def get_external_link(self, external_link_id: int) -> ExternalLink:
        external_link = await self.external_link_port.get_external_link(external_link_id)
        if not external_link:
            raise ValueError(f"Link con ID {external_link_id} no encontrado")
        return external_link

    async def get_student_external_links(self, student_id: int) -> List[ExternalLink]:
        external_link = await self.external_link_port.get_external_links_by_student_id(student_id)
        if not external_link:
            raise ValueError(f"No se encontraron links para el estudiante con ID {student_id}")
        return external_link

    async def get_all_external_links(self) -> List[ExternalLink]:
        return await self.external_link_port.get_all_external_links()

    async def update_external_link(self, external_link_id: int, external_link_data: Dict[str, Any]) -> ExternalLink:
        external_link = await self.external_link_port.get_external_link(external_link_id)
        if not external_link:
            raise ValueError(f"Link con ID {external_link_id} no encontrado")

        updated_external_link = await self.external_link_port.update_external_link(external_link_id, external_link_data)
        if not updated_external_link:
            raise ValueError(f"Error al actualizar el link con ID {external_link_id}")

        return updated_external_link

    async def delete_external_link(self, external_link_id: int) -> Dict[str, Any]:
        external_link = await self.external_link_port.get_external_link(external_link_id)
        if not external_link:
            raise ValueError(f"Link con ID {external_link_id} no encontrado")

        success = await self.external_link_port.delete_external_link(external_link_id)
        if not success:
            raise ValueError(f"Error al eliminar el link con ID {external_link_id}")

        return {
            "message": "Link eliminado exitosamente"
        }