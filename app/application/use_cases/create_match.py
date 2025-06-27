from app.domain.entities.filter_match import FilterMatch
from app.application.ports.create_match_port import CreateMatchPort
from app.domain.entities.student import Student

class CreateMatchUseCase:
    def __init__(self, createMatchUseCase: CreateMatchPort):
        self.createMatchUseCase = createMatchUseCase

    async def execute(self, student: Student ,filterMatch: FilterMatch):
        result = await self.createMatchUseCase.match_job_student(student, filterMatch)
        return result