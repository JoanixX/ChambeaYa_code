from abc import ABC, abstractmethod

class RegisterStudentPort(ABC):
    @abstractmethod
    async def register(self, *, name: str, email: str, date_of_birth, enrollment_date, session):
        pass
