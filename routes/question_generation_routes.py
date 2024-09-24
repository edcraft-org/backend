from fastapi import APIRouter, HTTPException
from typing import List
from utils.topics_helper import TOPIC_SUBTOPIC_MAPPING

question_generation_router = APIRouter()

@question_generation_router.post("/generate/{topic}/{subtopic}")
async def generate_question(topic: str, subtopic: str):
    question_class = TOPIC_SUBTOPIC_MAPPING.get((topic, subtopic))
    if question_class is None:
        raise HTTPException(status_code=400, detail="Invalid topic or subtopic")
    return None
    # question = question_class()
    # try:
    #     question.obtain_input(values)
    #     question.process_method()
    # except ValueError as e:
    #     raise HTTPException(status_code=400, detail=str(e))

    # new_question = Question(**question.model_dump())
    # await new_question.insert()
    # return new_question