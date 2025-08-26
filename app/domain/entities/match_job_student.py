from datetime import datetime

class MatchJobStudent:
    def __init__(self, id: int, student_id: int, job_offer_id: int, score: float, match_date: datetime,
                 rank: int, updated_at: datetime = None, deleted_at: datetime = None):
        self.id = id
        self.student_id = student_id
        self.job_offer_id = job_offer_id
        self.score = score
        self.match_date = match_date
        self.rank = rank
        self.updated_at = updated_at
        self.deleted_at = deleted_at