class MatchJobStudent:
    def __init__(self, id: int, student_id: int, job_offer_id: int, score: float, match_date, rank: int):
        self.id = id
        self.student_id = student_id
        self.job_offer_id = job_offer_id
        self.score = score
        self.match_date = match_date
        self.rank = rank
