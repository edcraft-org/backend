from fastapi import APIRouter, HTTPException
from typing import List, Optional
from models import QuestionBank, QuestionBankCreate, AddQuestionToQuestionBank, QuestionBankTitleUpdate, Question
from beanie import PydanticObjectId

from models.question_bank import QuestionBankWithQuestions

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


@question_bank_router.get("/{question_bank_id}", response_model=QuestionBankWithQuestions)
async def get_question_bank_with_questions(question_bank_id: str):
    question_bank = await QuestionBank.get(question_bank_id)
    if not question_bank:
        raise HTTPException(status_code=404, detail="Question bank not found")
    valid_question_ids = [PydanticObjectId(q_id) for q_id in question_bank.questions if PydanticObjectId.is_valid(q_id)]
    full_questions = await Question.find({"_id": {"$in": valid_question_ids}}).to_list()

    response = QuestionBankWithQuestions.construct(
        **question_bank.dict(),
        full_questions=full_questions
    )
    return response


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


@question_bank_router.delete("/{question_bank_id}/questions/{question_id}", response_model=str)
async def remove_question_from_question_bank(question_bank_id: str, question_id: str):
    question_bank = await QuestionBank.get(question_bank_id)
    if not question_bank:
        raise HTTPException(status_code=404, detail="Question bank not found")

    if question_id not in question_bank.questions:
        raise HTTPException(status_code=404, detail="Question not found in the question bank")

    question_bank.questions.remove(question_id)
    await question_bank.save()
    return f"Question {question_id} removed from question bank {question_bank_id} successfully"


@question_bank_router.delete("/{question_bank_id}", response_model=str)
async def delete_question_bank(question_bank_id: str):
    question_bank = await QuestionBank.get(question_bank_id)
    if not question_bank:
        raise HTTPException(status_code=404, detail="Question bank not found")
    await question_bank.delete()
    return f"Question bank {question_bank_id} deleted successfully"


@question_bank_router.put("/{question_bank_id}/title", response_model=QuestionBank)
async def rename_question_bank_title(question_bank_id: str, title_update: QuestionBankTitleUpdate):
    question_bank = await QuestionBank.get(question_bank_id)
    if not question_bank:
        raise HTTPException(status_code=404, detail="Question bank not found")
    question_bank.title = title_update.title
    await question_bank.save()
    return question_bank
