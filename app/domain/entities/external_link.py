from datetime import datetime

class ExternalLink:
    def __init__(self, id: int, student_id: int, link: str, created_at: datetime = None, updated_at: datetime = None):
        self.id = id
        self.student_id = student_id
        self.link = link
        self.created_at = created_at
        self.updated_at = updated_at