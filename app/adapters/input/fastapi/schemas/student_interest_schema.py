from pydantic import BaseModel, Field

class StudentInterestCreate(BaseModel):
    student_id: int = Field(..., description="ID of the student")
    interest_id: int = Field(..., description="ID of the interest")

class StudentInterestResponse(BaseModel):
    student_id: int
    interest_id: int