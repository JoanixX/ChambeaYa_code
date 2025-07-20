from app.application.ports.register_company_port import RegisterCompanyPort
from app.domain.entities.company import Company
from app.domain.services.company_needs_analyzer import CompanyNeedsAnalyzer

class RegisterCompanyUseCase:
    def __init__(self, register_company_port: RegisterCompanyPort, company_analyzer: CompanyNeedsAnalyzer):
        self.register_company_port = register_company_port
        self.company_analyzer = company_analyzer

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
        
        # Crear entidad de dominio
        company = Company(
            RUC=company_data["RUC"],
            name=company_data["name"],
            location=company_data["location"],
            industry=company_data["industry"],
            area_id=company_data["area_id"],
            contact_name=company_data["contact_name"],
            email=company_data["email"],
            company_culture=company_data["company_culture"]
        )
        
        # Registrar empresa
        saved_company = await self.register_company_port.register_company(company)
        
        # Analizar necesidades
        analysis = await self.company_analyzer.analyze_company_needs(saved_company.id)
        
        return {
            "company_id": saved_company.id,
            "registration_success": True,
            "needs_analysis": analysis
        }
