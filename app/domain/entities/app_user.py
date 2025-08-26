import enum
from datetime import date, datetime

class UserRole(enum.Enum):
    admin = 'admin'
    company = 'company'
    student = 'student'

class AppUser:
    def __init__(self, id: int, email: str, dni: str, password_hash: str, role: UserRole, related_id: int,
                 created_at: datetime, updated_at: datetime, deleted_at: datetime = None,
                 cv_url: str = None, name: str = None, location: str = None, ruc: str = None,
                 date_of_birth: date = None, main_motivation: str = None, description: str = None):
        self.id = id
        self.email = email
        self.dni = dni
        self.cv_url = cv_url
        self.name = name
        self.location = location
        self.ruc = ruc
        self.date_of_birth = date_of_birth
        self.main_motivation = main_motivation
        self.description = description
        self.password_hash = password_hash
        self.role = role
        self.related_id = related_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at