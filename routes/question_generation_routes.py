from pathlib import Path
from typing import Any, Dict, List, Type
from fastapi import APIRouter, Depends, HTTPException
from models import GenerateQuestionRequest
from question.queryable_class import QueryableClass
from question.processor_class import ProcessorClass
from utils.question_generation_helper import (
    autoload_classes, autoload_queryable_classes, generate_question, 
    list_queryable, list_subtopics, list_topics, list_variable
)

question_generation_router = APIRouter()

def get_autoloaded_classes() -> Dict[str, Dict[str, Type[ProcessorClass]]]:
    base_package = 'question.processor_subclasses'
    base_path = Path(__file__).resolve().parent.parent / 'question' / 'processor_subclasses'
    return autoload_classes(str(base_path), base_package)

def get_autoloaded_queryable_classes() -> Dict[str, Type[QueryableClass]]:
    base_package = 'question'
    base_path = Path(__file__).resolve().parent.parent
    return autoload_queryable_classes(str(base_path), base_package)

def handle_exceptions(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    return wrapper

@question_generation_router.get("/topics")
@handle_exceptions
async def get_topics_route(autoloaded_classes: Dict[str, Dict[str, Type[ProcessorClass]]] = Depends(get_autoloaded_classes)) -> List[str]:
    return list_topics(autoloaded_classes)

@question_generation_router.get("/topics/{topic}/subtopics")
@handle_exceptions
async def get_subtopics_route(topic: str, autoloaded_classes: Dict[str, Dict[str, Type[ProcessorClass]]] = Depends(get_autoloaded_classes)) -> List[str]:
    return list_subtopics(autoloaded_classes, topic)

@question_generation_router.get("/topics/{topic}/subtopics/{subtopic}/queryables")
@handle_exceptions
async def list_queryables_route(topic: str, subtopic: str, autoloaded_classes: Dict[str, Dict[str, Type[ProcessorClass]]] = Depends(get_autoloaded_classes)) -> List[str]:
    return list_queryable(autoloaded_classes, topic, subtopic)

@question_generation_router.get("/queryable_classes")
@handle_exceptions
async def get_queryable_classes_route(queryable_classes: Dict[str, Type[QueryableClass]] = Depends(get_autoloaded_queryable_classes)) -> List[str]:
    return list(queryable_classes.keys())

@question_generation_router.get("/topics/{topic}/subtopics/{subtopic}/queryables/{queryable}/variables")
@handle_exceptions
async def list_variables_route(topic: str, subtopic: str, queryable: str, autoloaded_classes: Dict[str, Dict[str, Type[ProcessorClass]]] = Depends(get_autoloaded_classes)) -> List[str]:
    return list_variable(autoloaded_classes, topic, subtopic, queryable)

@question_generation_router.post("/generate")
@handle_exceptions
async def generate_route(request: GenerateQuestionRequest, autoloaded_classes: Dict[str, Dict[str, Type[ProcessorClass]]] = Depends(get_autoloaded_classes)):
    results = []
    for _ in range(request.number_of_questions):
        generated_question = generate_question(
            autoloaded_classes, request.topic, request.subtopic, 
            request.queryable, request.number_of_options, request.question_description
        )

        if generated_question is None:
            raise HTTPException(status_code=500, detail="Failed to generate question.")

        results.append({
            **generated_question,
            "marks": request.marks,
        })
    return results
