from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from typing import List, Optional

class Assessment(Document):
    id: Optional[PydanticObjectId] = Field(None, alias="_id", description="The unique identifier of the assessment")
    title: str = Field(..., description="The title of the assessment")
    questions: List[str] = Field(..., description="List of question IDs")
    user_id: str = Field(..., description="The ID of the user who created the assessment")

    class Settings:
        name = "assessments"

class AssessmentCreate(BaseModel):
    title: str = Field(..., description="The title of the assessment")
    user_id: str = Field(..., description="The ID of the user who created the assessment")
    questions: Optional[List[str]] = Field(default_factory=list, description="List of question IDs")

class AddQuestionToAssessment(BaseModel):
    question_id: str = Field(..., description="The ID of the question to add to the assessment")