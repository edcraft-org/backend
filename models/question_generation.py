from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional

class ContextRequest(BaseModel):
    selectedTopic: str
    selectedSubtopic: str
    inputPath: Dict[str, Any]
    selectedSubclasses: Dict[str, str]
    selectedQuantifiables: Dict[str, str]
    arguments: Dict[str, Any]
    inputArguments: Dict[str, Any]
    argumentsInit: Optional[Dict[str, Any]]
    inputInit: Optional[Dict[str, Any]]
    userAlgoCode: Optional[str]
    userEnvCode: Optional[str]

class QuestionDetails(BaseModel):
    marks: float
    number_of_options: int
    # question_type: str

class SubQuestion(BaseModel):
    description: str
    queryable: str
    inputQueryable: str
    context: ContextRequest
    questionDetails: QuestionDetails
    userQueryableCode: Optional[str]

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
    arguments_init: Optional[Dict[str, Any]] = None
    userAlgoCode: Optional[str] = None

class VariableResponse(BaseModel):
    context: Dict[str, Any]
    context_init: Dict[str, Any]

class UserQueryableRequest(BaseModel):
    userAlgoCode: str

class InputRequest(BaseModel):
    input_path: Dict[str, Any]

class GenerateInputRequest(BaseModel):
    input_path: Dict[str, Any]
    variable_options: Dict[str, Any]
    input_init: Optional[Dict[str, Any]] = None
