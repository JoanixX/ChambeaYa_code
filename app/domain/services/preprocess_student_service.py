from app.infraestructure.ai_client.ai_connection import preprocess_all_students
from app.domain.entities.student import Student
from typing import List

class PreprocessStudentService:
    async def preprocess_all(self, students: List[Student]):
        students_data = []
        for s in students:
            students_data.append({
                "id": s.id,
                "name": s.name,
                "email": s.email,
                "career": s.career,
                "academic_cycle": s.academic_cycle,
                "location": s.location,
                "main_motivation": s.main_motivation,
                "description": s.description,
                "weekly_availability": s.weekly_availability,
                "preferred_modality": s.preferred_modality,
                "experience_id": s.experience_id,
                "date_of_birth": s.date_of_birth.isoformat() if s.date_of_birth else None,
                "embedding": None
            })
        return await preprocess_all_students(students_data)
