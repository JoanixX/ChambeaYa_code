from app.domain.entities.company import Company
from app.domain.repositories.company_repository import CompanyRepository
from app.application.ports.register_company_port import RegisterCompanyPort

class RegisterCompanyService:
    def __init__(self, company_repo: CompanyRepository, register_company_port: RegisterCompanyPort):
        self.company_repo = company_repo
        self.register_company_port = register_company_port

    async def register_company(self, company_data: dict):
        # Validaciones de negocio básicas
        if await self.company_repo.find_by_ruc(company_data["RUC"]):
            raise ValueError("El RUC ya está registrado")
        
        if await self.company_repo.find_by_email(company_data["email"]):
            raise ValueError("El email ya está registrado")
        
        # Crear entidad de dominio con constructor correcto
        company = Company(
            id=0,  # Se asignará automáticamente por la base de datos
            RUC=company_data["RUC"],
            name=company_data["name"],
            location=company_data["location"],
            industry=company_data["industry"],
            area_id=company_data["area_id"],
            contact_name=company_data["contact_name"],
            email=company_data["email"],
            company_culture=company_data["company_culture"]
        )
        
        # Guardar empresa usando el repositorio directamente
        saved_model = await self.company_repo.save(company)
        if saved_model:
            return saved_model.id  # Retornar solo el ID
        else:
            raise ValueError("Error al guardar la empresa")