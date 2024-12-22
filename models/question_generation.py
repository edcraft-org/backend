from typing import Any, Dict
from pydantic import BaseModel


class GenerateQuestionRequest(BaseModel):
    topic: str
    subtopic: str
    queryable: str
    element_type: Dict[str, str]
    subclasses: Dict[str, str]
    arguments: Dict[str, Any]
    question_description: str
    question_type: str
    marks: float
    number_of_options: int
    number_of_questions: int
