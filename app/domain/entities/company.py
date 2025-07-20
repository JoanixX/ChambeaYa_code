class Company:
    def __init__(self, id: int, RUC: str, name: str, location: str, industry: str, area_id: int, contact_name: str, email: str, company_culture: str):
        self.id = id
        self.RUC = RUC
        self.name = name
        self.location = location
        self.industry = industry
        self.area_id = area_id
        self.contact_name = contact_name
        self.email = email
        self.company_culture = company_culture