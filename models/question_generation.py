from typing import Dict
from pydantic import BaseModel


class GenerateQuestionRequest(BaseModel):
    topic: str
    subtopic: str
    queryable: str
    element_type: Dict[str, str]
    subclasses: Dict[str, str]
    question_description: str
    question_type: str
    marks: float
    number_of_options: int
    number_of_questions: int
