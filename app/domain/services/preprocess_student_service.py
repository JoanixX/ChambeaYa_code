from app.infraestructure.ai_client.ai_connection import preprocess_all_students
from app.infraestructure.ai_client.ai_connection import preprocess_student
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

    async def preprocess_student(self, student: Student):
        student_data = {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "career": student.career,
            "academic_cycle": student.academic_cycle,
            "location": student.location,
            "main_motivation": student.main_motivation,
            "description": student.description,
            "weekly_availability": student.weekly_availability,
            "preferred_modality": student.preferred_modality,
            "experience_id": student.experience_id,
            "date_of_birth": student.date_of_birth.isoformat() if student.date_of_birth else None,
            "embedding": None
        }
        return await preprocess_student(student_data)