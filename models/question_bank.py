from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from typing import List, Optional

class QuestionBank(Document):
    id: Optional[PydanticObjectId] = Field(None, alias="_id", description="The unique identifier of the question bank")
    title: str = Field(..., description="The title of the question bank")
    questions: List[str] = Field(..., description="List of question IDs")
    user_id: str = Field(..., description="The ID of the user who created the question bank")
    project_id: str = Field(..., description="The ID of the project associated with the question bank")

    class Settings:
        name = "question_banks"

class QuestionBankCreate(BaseModel):
    title: str = Field(..., description="The title of the question bank")
    questions: Optional[List[str]] = Field(default_factory=list, description="List of question IDs")
    user_id: str = Field(..., description="The ID of the user who created the question bank")
    project_id: str = Field(..., description="The ID of the project associated with the question bank")

class AddQuestionToQuestionBank(BaseModel):
    question_id: str = Field(..., description="The ID of the question to add to the question bank")

class QuestionBankTitleUpdate(BaseModel):
    title: str