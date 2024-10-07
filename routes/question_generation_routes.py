from fastapi import APIRouter, HTTPException
from utils.topics_helper import get_topics, get_topic_class
from models import GenerateQuestionRequest

question_generation_router = APIRouter()

@question_generation_router.get("/topics")
async def list_topics():
    return get_topics()

@question_generation_router.get("/topics/{topic}/subtopics")
async def list_subtopics(topic: str):
    try:
        topic_class = get_topic_class(topic)
        return topic_class.subtopic()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@question_generation_router.get("/topics/{topic}/subtopics/{subtopic}/queryables")
async def list_queryables(topic: str, subtopic: str):
    try:
        topic_class = get_topic_class(topic)
        return topic_class.queryable_options()
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
        # question_class = get_question_class(request.topic, request.subtopic)
        topic_class = get_topic_class(request.topic)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    questions_and_answers = []

    for _ in range(request.number_of_questions):
        # Obtain input variables and options data
        variables_data, options_data = topic_class.obtain_input(request.number_of_options)

        # Process the method to get the answer and options
        result = topic_class.process_method(request.queryable, request.subtopic, variables_data, options_data)


        # Format the question description
        queryable_options = topic_class.queryable_options()
        topic_item = next((item for item in queryable_options if item['queryable'] == request.queryable), None)
        if not topic_item:
            raise ValueError(f"Queryable {request.queryable} not found in queryable options")
        queryable_variables = topic_item['variables']

        question_text = topic_class.format_question_description(queryable_variables, request.question_description, variables_data)

        questions_and_answers.append({
            "question": question_text,
            "answer": result["answer"],
            "marks": request.marks,
            "options": result["options"]
        })

    return questions_and_answers
