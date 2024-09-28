from fastapi import APIRouter, HTTPException
from utils.topics_helper import get_question_class, get_topics, get_subtopics
from models import GenerateQuestionRequest

question_generation_router = APIRouter()

@question_generation_router.get("/topics")
async def list_topics():
    return get_topics()

@question_generation_router.get("/topics/{topic}/subtopics")
async def list_subtopics(topic: str):
    try:
        return get_subtopics(topic)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@question_generation_router.get("/topics/{topic}/subtopics/{subtopic}/queryables")
async def list_queryables(topic: str, subtopic: str):
    try:
        question_class = get_question_class(topic, subtopic)
        return question_class.query_options()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# @question_generation_router.get("/topics/{topic}/subtopics/{subtopic}/queryables/{queryable}/variables")
# async def list_variables(topic: str, subtopic: str, queryable: str):
#     try:
#         question_class = get_question_class(topic, subtopic)
#         return question_class.variables(queryable)
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))

@question_generation_router.post("/generate")
async def generate_question(request: GenerateQuestionRequest):
    try:
        question_class = get_question_class(request.topic, request.subtopic)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    input_type = question_class.input_type()
    query_options = question_class.query_options()
    output_type = question_class.output_type('Preorder')  # Example method name

    return {
        "input_type": input_type,
        "query_options": query_options,
        "output_type": output_type,
        "number_of_options": request.number_of_options,
        "number_of_questions": request.number_of_questions
    }