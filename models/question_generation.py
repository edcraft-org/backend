from pydantic import BaseModel

class GenerateQuestionRequest(BaseModel):
    topic: str
    subtopic: str
    queryable: str
    question_description: str
    question_type: str
    number_of_options: int
    number_of_questions: int