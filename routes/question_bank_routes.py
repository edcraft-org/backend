from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from models.question_bank import QuestionBank, QuestionBankCreate, AddQuestionToQuestionBank
from models.question import Question
from beanie import PydanticObjectId

question_bank_router = APIRouter()

@question_bank_router.post("/", response_model=QuestionBank)
async def add_question_bank(question_bank: QuestionBankCreate):
    new_question_bank = QuestionBank(**question_bank.model_dump())
    await new_question_bank.insert()
    return new_question_bank

@question_bank_router.get("/", response_model=List[QuestionBank])
async def get_question_banks(user_id: Optional[str] = None, project_id: Optional[str] = None):
    query = {}
    if user_id:
        query['user_id'] = user_id
    if project_id:
        query['project_id'] = project_id
    question_banks = await QuestionBank.find(query).to_list()
    return question_banks

@question_bank_router.get("/{question_bank_id}", response_model=QuestionBank)
async def get_question_bank_with_questions(question_bank_id: str):
    question_bank = await QuestionBank.get(question_bank_id)
    if not question_bank:
        raise HTTPException(status_code=404, detail="Question bank not found")
    valid_question_ids = [PydanticObjectId(q_id) for q_id in question_bank.questions if PydanticObjectId.is_valid(q_id)]
    questions = await Question.find({"_id": {"$in": valid_question_ids}}).to_list()
    question_bank.questions = questions
    return question_bank

@question_bank_router.post("/{question_bank_id}/questions", response_model=str)
async def add_existing_question_to_question_bank(question_bank_id: str, data: AddQuestionToQuestionBank):
    question_bank = await QuestionBank.get(question_bank_id)
    if not question_bank:
        raise HTTPException(status_code=404, detail="Question bank not found")

    question = await Question.get(data.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    question_bank.questions.append(data.question_id)
    await question_bank.save()
    return str(data.question_id)