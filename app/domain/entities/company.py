from datetime import datetime

class Company:
    def __init__(self, id: int, name: str, industry: str, company_culture: str,
                 created_at: datetime, updated_at: datetime, deleted_at: datetime = None):
        self.id = id
        self.name = name
        self.industry = industry
        self.company_culture = company_culture
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at