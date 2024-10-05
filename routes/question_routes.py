from fastapi import APIRouter, HTTPException, Depends
from models.question import Question, QuestionCreate
from beanie import PydanticObjectId

question_router = APIRouter()

@question_router.post("/", response_model=Question)
async def add_question(question: QuestionCreate):
    new_question = Question(**question.model_dump())
    await new_question.insert()
    return new_question

@question_router.get("/{question_id}", response_model=Question)
async def get_question_by_id(question_id: str):
    question = await Question.get(PydanticObjectId(question_id))
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@question_router.delete("/{question_id}", response_model=str)
async def delete_question(question_id: str):
    question = await Question.get(PydanticObjectId(question_id))
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    await question.delete()
    return f"Question {question_id} deleted successfully"