import enum

class UserRole(enum.Enum):
    admin = 'admin'
    company = 'company'
    student = 'student'

class AppUser:
    def __init__(self, id: int, email: str, password_hash: str, role: UserRole, related_id: int):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.related_id = related_id
