from pydantic import BaseModel, Field
from typing import Any, Dict, List, Literal, Optional

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
    userEnvCode: Optional[List[str]]

class QuestionDetails(BaseModel):
    marks: float
    number_of_options: int
    # question_type: str

class SubQuestionContext(BaseModel):
    description: str
    queryable: str
    inputQueryable: str
    context: ContextRequest
    questionDetails: QuestionDetails
    userQueryableCode: Optional[str]

class GenerateQuestionRequest(BaseModel):
    description: str
    context: ContextRequest
    sub_questions: Optional[List[SubQuestionContext]] = Field(None, description="List of subquestions")

class GenerateVariableRequest(BaseModel):
    topic: str
    subtopic: str
    element_type: Dict[str, str]
    subclasses: Dict[str, str]
    arguments: Dict[str, Any]
    question_description: str
    arguments_init: Optional[Dict[str, Any]] = None
    userAlgoCode: Optional[str] = None
    userEnvCode: Optional[List[str]] = None

class VariableResponse(BaseModel):
    context: Dict[str, Any]
    context_init: Dict[str, Any]
    has_output: bool
    cls_name: Optional[str] = None

class OutputResponse(BaseModel):
    output_init: Dict[str, Any]
    output_path: Dict[str, Any]
    context: Dict[str, Any]
    user_env_code: Optional[str] = None

class UserQueryableRequest(BaseModel):
    userAlgoCode: str
    userEnvCode: Optional[List[str]] = None

class UserInputVariableRequest(BaseModel):
    userEnvCode: str

class InputRequest(BaseModel):
    input_path: Dict[str, Any]

class GenerateInputRequest(BaseModel):
    input_path: Dict[str, Any]
    variable_options: Dict[str, Any]
    element_type: Dict[str, str]
    input_init: Optional[Dict[str, Any]] = None
    user_env_code: Optional[str] = None

class GeneratedContextItem(BaseModel):
    id: str = Field(..., description="The unique identifier of the context item")
    type: Literal['input', 'algo'] = Field(..., description="The type of the context")
    context: Dict[str, Any] = Field(..., description="The context data")
    context_init: Dict[str, Any] = Field(..., description="The context initialization data")
    has_output: bool = Field(..., description="Whether the context has output")
    name: Optional[str] = Field(None, description="Optional name for the context")
