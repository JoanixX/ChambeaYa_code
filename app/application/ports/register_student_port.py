from abc import ABC, abstractmethod

class RegisterStudentPort(ABC):
    @abstractmethod
    async def register(self, *, name: str, email: str, date_of_birth, experience_id: int, location: str, weekly_availability: int, preferred_modality: int, career: str, academic_cycle: int, main_motivation: str, description: str, session):
        pass
