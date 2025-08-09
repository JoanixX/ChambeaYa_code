from datetime import datetime

class Company:
    def __init__(self, id: int, ruc: str, name: str,
                 location: str, industry: str,
                 area_id: int, contact_name: str,
                 email: str, company_culture: str,
                 created_at: datetime, updated_at: datetime,
                 deleted_at: datetime = None):
        self.id = id
        self.ruc = ruc
        self.name = name
        self.location = location
        self.industry = industry
        self.area_id = area_id
        self.contact_name = contact_name
        self.email = email
        self.company_culture = company_culture
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at