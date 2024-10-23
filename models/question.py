from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from typing import List, Optional


class Question(Document):
    id: Optional[PydanticObjectId] = Field(None, alias="_id", description="The unique identifier of the question")
    text: str
    options: List[str]
    answer: str
    user_id: str
    marks: float = Field(..., description="The marks assigned to the question")

    class Settings:
        name = "questions"


class QuestionCreate(BaseModel):
    text: str = Field(..., description="The text of the question")
    options: List[str] = Field(..., description="List of options for the question")
    answer: str = Field(..., description="The correct answer for the question")
    user_id: str = Field(..., description="The ID of the user who created the question")
    marks: float = Field(..., description="The marks assigned to the question")
