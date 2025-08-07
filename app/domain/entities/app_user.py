import enum
from datetime import date, datetime

class UserRole(enum.Enum):
    admin = 'admin'
    company = 'company'
    student = 'student'

class AppUser:
    def __init__(self, id: int, email: str, dni: str, cv_url: str, name: str, location: str, RUC: str, date_of_birth: date, password_hash: str, role: UserRole, related_id: int, created_at: datetime, updated_at: datetime, deleted_at: datetime = None):
        self.id = id
        self.email = email
        self.dni = dni
        self.cv_url = cv_url
        self.name = name
        self.location = location
        self.RUC = RUC
        self.date_of_birth = date_of_birth
        self.password_hash = password_hash
        self.role = role
        self.related_id = related_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
