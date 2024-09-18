from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from models.assessment import Assessment, AssessmentCreate, AddQuestionToAssessment
from models.question import Question
from beanie import PydanticObjectId

assessment_router = APIRouter()

@assessment_router.post("/", response_model=Assessment)
async def add_assessment(assessment: AssessmentCreate):
    new_assessment = Assessment(**assessment.model_dump())
    await new_assessment.insert()
    return new_assessment

@assessment_router.get("/", response_model=List[Assessment])
async def get_assessments(user_id: Optional[str] = None):
    query = {}
    if user_id:
        query['user_id'] = user_id
    assessments = await Assessment.find(query).to_list()
    return assessments

@assessment_router.get("/{assessment_id}", response_model=Assessment)
async def get_assessment_with_questions(assessment_id: str):
    assessment = await Assessment.get(assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    valid_question_ids = [PydanticObjectId(q_id) for q_id in assessment.questions if PydanticObjectId.is_valid(q_id)]
    questions = await Question.find({"_id": {"$in": valid_question_ids}}).to_list()
    assessment.questions = questions
    return assessment

@assessment_router.post("/{assessment_id}/questions", response_model=str)
async def add_existing_question_to_assessment(assessment_id: str, data: AddQuestionToAssessment):
    assessment = await Assessment.get(assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    question = await Question.get(data.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    if data.question_id in assessment.questions:
        raise HTTPException(status_code=400, detail="Question already added to the assessment")

    assessment.questions.append(data.question_id)
    await assessment.save()
    return str(data.question_id)