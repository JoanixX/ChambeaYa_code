from abc import ABC, abstractmethod

class RegisterCompanyPort(ABC):
    @abstractmethod
    async def register(self, *, name: str, industry: str, contact_name: str, email: str, session):
        pass
