from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from typing import Dict, List, Optional

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class SubQuestion(BaseModel):
    description: str = Field(..., description="The description of the subquestion")
    options: List[str] = Field(..., description="List of options for the subquestion")
    answer: str = Field(..., description="The correct answer for the subquestion")
    marks: float = Field(..., description="The marks assigned to the subquestion")
    svg: Optional[Dict[str, str]] = Field(None, description="The SVG representations of the subquestion")
    answer_svg: Optional[Dict[str, str]] = Field(None, description="The SVG representations of the answer")

class Question(Document):
    id: Optional[PydanticObjectId] = Field(None, alias="_id", description="The unique identifier of the question")
    user_id: str = Field(..., description="The ID of the user who created the question")
    description: str = Field(..., description="The outer description of the question")
    svg: Optional[Dict[str, str]] = Field(None, description="The SVG representations of the question")
    subquestions: Optional[List[SubQuestion]] = Field(None, description="List of subquestions")

    class Settings:
        name = "questions"

class QuestionCreate(BaseModel):
    user_id: str = Field(..., description="The ID of the user who created the question")
    description: str = Field(..., description="The outer description of the question")
    svg: Optional[Dict[str, str]] = Field(None, description="The SVG representations of the question")
    subquestions: Optional[List[SubQuestion]] = Field(None, description="List of subquestions")
