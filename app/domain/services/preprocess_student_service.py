from app.infraestructure.ai_client.ai_connection import preprocess_all_students
from app.infraestructure.ai_client.ai_connection import preprocess_student
from app.domain.entities.student import Student
from typing import List
from app.adapters.output.orm.repositories.experience_detail_repository_impl import get_experience_name_by_id_impl

class PreprocessStudentService:
    async def preprocess_all(self, students: List[Student], session):
        from sqlalchemy.future import select
        from app.adapters.output.orm.models.student_skill_model import StudentSkillModel
        from app.adapters.output.orm.models.student_interest_model import StudentInterestModel
        from app.adapters.output.orm.repositories.skill_repository_impl import get_skill_by_id_impl
        from app.adapters.output.orm.models.interest_model import InterestModel
        students_data = []
        for s in students:
            experience_name = None
            if s.experience_id:
                experience_name = await get_experience_name_by_id_impl(session, s.experience_id)

            # Fetch skills
            skill_links_result = await session.execute(select(StudentSkillModel).where(StudentSkillModel.student_id == s.id))
            skill_links = skill_links_result.scalars().all()
            skills = []
            for link in skill_links:
                skill = await get_skill_by_id_impl(session, link.skill_id)
                if skill:
                    skills.append(skill.name)

            # Fetch interests
            interest_links_result = await session.execute(select(StudentInterestModel).where(StudentInterestModel.student_id == s.id))
            interest_links = interest_links_result.scalars().all()
            interests = []
            for link in interest_links:
                interest_result = await session.execute(select(InterestModel).where(InterestModel.id == link.interest_id))
                interest_obj = interest_result.scalar_one_or_none()
                if interest_obj:
                    interests.append(interest_obj.name)

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
                # "experience": experience_name, -> asi debe ser originalmente, el id pasa un numero nomas
                "experience_id": s.experience_id,
                "skills": skills,
                "interests": interests,
                "date_of_birth": s.date_of_birth.isoformat() if s.date_of_birth else None,
                "embedding": None
            })
        result = await preprocess_all_students(students_data)
        return result

    async def preprocess_student(self, student: Student, session):
        from sqlalchemy.future import select
        from app.adapters.output.orm.models.student_skill_model import StudentSkillModel
        from app.adapters.output.orm.models.student_interest_model import StudentInterestModel
        from app.adapters.output.orm.repositories.skill_repository_impl import get_skill_by_id_impl
        from app.adapters.output.orm.models.interest_model import InterestModel

        experience_name = None
        if student.experience_id:
            experience_name = await get_experience_name_by_id_impl(session, student.experience_id)

        # Fetch skills
        skill_links_result = await session.execute(select(StudentSkillModel).where(StudentSkillModel.student_id == student.id))
        skill_links = skill_links_result.scalars().all()
        skills = []
        for link in skill_links:
            skill = await get_skill_by_id_impl(session, link.skill_id)
            if skill:
                skills.append(skill.name)

        # Fetch interests
        interest_links_result = await session.execute(select(StudentInterestModel).where(StudentInterestModel.student_id == student.id))
        interest_links = interest_links_result.scalars().all()
        interests = []
        for link in interest_links:
            interest_result = await session.execute(select(InterestModel).where(InterestModel.id == link.interest_id))
            interest_obj = interest_result.scalar_one_or_none()
            if interest_obj:
                interests.append(interest_obj.name)

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
            "experience": experience_name,
            "experience_id": student.experience_id,
            "skills": skills,
            "interests": interests,
            "date_of_birth": student.date_of_birth.isoformat() if student.date_of_birth else None,
            "embedding": None
        }
        result = await preprocess_student(student_data)
        return result