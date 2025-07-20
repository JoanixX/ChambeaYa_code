from app.domain.entities.company import Company
from app.domain.repositories.company_repository import CompanyRepository
from app.application.ports.register_company_port import RegisterCompanyPort

class CompanyNeedsAnalyzer:
    def __init__(self, company_repo: CompanyRepository, register_company_port: RegisterCompanyPort):
        self.company_repo = company_repo
        self.register_company_port = register_company_port

    async def register_company(self, company_data: dict):
        # Validaciones de negocio
        if await self.company_repo.find_by_ruc(company_data["RUC"]):
            raise ValueError("El RUC ya está registrado")
        
        if await self.company_repo.find_by_email(company_data["email"]):
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
        
        # Guardar empresa
        saved_company = await self.company_repo.save(company)
        return saved_company

    async def analyze_company_needs(self, company_id: int):
        company = await self.company_repo.find_by_id(company_id)
        if not company:
            raise ValueError("Empresa no encontrada")
        
        # Lógica de análisis de necesidades
        analysis = {
            "company_id": company.id,
            "industry_analysis": self._analyze_industry(company),
            "location_analysis": self._analyze_location(company),
            "culture_fit": self._analyze_culture_fit(company),
            "recommendations": self._generate_company_recommendations(company)
        }
        
        return analysis

    def _analyze_industry(self, company: Company) -> dict:
        # Análisis basado en la industria
        industry_analysis = {
            "tech_industries": ["technology", "software", "it", "digital"],
            "finance_industries": ["finance", "banking", "insurance"],
            "healthcare_industries": ["healthcare", "medical", "pharmaceutical"],
            "education_industries": ["education", "training", "academic"]
        }
        
        company_industry = company.industry.lower()
        
        for category, industries in industry_analysis.items():
            if any(industry in company_industry for industry in industries):
                return {
                    "category": category,
                    "student_preferences": self._get_student_preferences_for_industry(category),
                    "skill_requirements": self._get_skill_requirements_for_industry(category)
                }
        
        return {
            "category": "general",
            "student_preferences": ["flexible", "adaptable"],
            "skill_requirements": ["communication", "teamwork"]
        }

    def _analyze_location(self, company: Company) -> dict:
        # Análisis basado en la ubicación
        location = company.location.lower()
        
        if "lima" in location or "peru" in location:
            return {
                "region": "lima",
                "student_availability": "high",
                "transportation_options": "good"
            }
        elif "provincia" in location:
            return {
                "region": "province",
                "student_availability": "medium",
                "transportation_options": "limited"
            }
        else:
            return {
                "region": "remote",
                "student_availability": "high",
                "transportation_options": "not_applicable"
            }

    def _analyze_culture_fit(self, company: Company) -> dict:
        # Análisis de cultura empresarial
        culture = company.company_culture.lower()
        
        culture_indicators = {
            "innovative": ["innovative", "creative", "startup", "dynamic"],
            "traditional": ["traditional", "established", "corporate", "formal"],
            "collaborative": ["collaborative", "team", "cooperative", "supportive"],
            "competitive": ["competitive", "results", "performance", "achievement"]
        }
        
        for culture_type, indicators in culture_indicators.items():
            if any(indicator in culture for indicator in indicators):
                return {
                    "culture_type": culture_type,
                    "student_profile_match": self._get_student_profile_for_culture(culture_type)
                }
        
        return {
            "culture_type": "balanced",
            "student_profile_match": "adaptable"
        }

    def _get_student_preferences_for_industry(self, industry_category: str) -> list[str]:
        preferences_map = {
            "tech_industries": ["programming", "analytical", "problem_solving"],
            "finance_industries": ["analytical", "detail_oriented", "reliable"],
            "healthcare_industries": ["caring", "detail_oriented", "patient"],
            "education_industries": ["teaching", "communication", "patience"]
        }
        return preferences_map.get(industry_category, ["adaptable"])

    def _get_skill_requirements_for_industry(self, industry_category: str) -> list[str]:
        skills_map = {
            "tech_industries": ["programming", "data_analysis", "problem_solving"],
            "finance_industries": ["excel", "financial_analysis", "attention_to_detail"],
            "healthcare_industries": ["medical_terminology", "patient_care", "documentation"],
            "education_industries": ["teaching", "curriculum_development", "student_management"]
        }
        return skills_map.get(industry_category, ["communication", "teamwork"])

    def _get_student_profile_for_culture(self, culture_type: str) -> str:
        profile_map = {
            "innovative": "creative_and_adaptable",
            "traditional": "structured_and_reliable",
            "collaborative": "team_oriented_and_supportive",
            "competitive": "results_driven_and_ambitious"
        }
        return profile_map.get(culture_type, "balanced")

    def _generate_company_recommendations(self, company: Company) -> list[str]:
        recommendations = []
        
        if not company.company_culture or len(company.company_culture) < 30:
            recommendations.append("Considera describir mejor la cultura de tu empresa para atraer candidatos más alineados")
        
        if "remote" not in company.location.lower():
            recommendations.append("Considera ofrecer opciones remotas para ampliar tu pool de candidatos")
        
        return recommendations