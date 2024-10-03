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

    questions_and_answers = []

    for _ in range(request.number_of_questions):
        # Obtain input variables and options data
        variables_data, options_data = question_class.obtain_input(request.queryable, request.number_of_options)

        # Process the method to get the answer and options
        result = question_class.process_method(request.queryable, variables_data, options_data)

        # # Format the question description
        # question_text = request.question_description.format(*variables_data)
        # Format the question description
        question_text = question_class.format_question_description(request.queryable, request.question_description, variables_data)


        questions_and_answers.append({
            "question": question_text,
            "answer": result["answer"],
            "marks": request.marks,
            "options": result["options"]
        })

    return questions_and_answers
