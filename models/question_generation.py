from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional

class ContextRequest(BaseModel):
    selectedTopic: str
    selectedSubtopic: str
    selectedSubclasses: Dict[str, str]
    selectedQuantifiables: Dict[str, str]
    arguments: Dict[str, Any]
    argumentsInit: Optional[Dict[str, Any]]

class QuestionDetails(BaseModel):
    marks: float
    number_of_options: int

class SubQuestion(BaseModel):
    description: str
    queryable: str
    context: ContextRequest
    questionDetails: QuestionDetails

class GenerateQuestionRequest(BaseModel):
    description: str
    context: ContextRequest
    sub_questions: Optional[List[SubQuestion]] = Field(None, description="List of subquestions")

class GenerateVariableRequest(BaseModel):
    topic: str
    subtopic: str
    element_type: Dict[str, str]
    subclasses: Dict[str, str]
    arguments: Dict[str, Any]
    question_description: str

class VariableResponse(BaseModel):
    context: Dict[str, Any]
    context_init: Dict[str, Any]
