from pathlib import Path
from typing import Dict, List, Type
from fastapi import APIRouter, Depends, HTTPException
from models import GenerateQuestionRequest
from question_generation.quantifiable.quantifiable_class import Quantifiable
from question_generation.queryable.queryable_class import Queryable
from question_generation.algo.algo import Algo
from utils.classes_helper import get_all_subclasses
from utils.question_generation_helper import (
    autoload_classes, generate_question,
    list_queryable, list_subtopics, list_topics, list_variable,
    GeneratedQuestionClassType
)

question_generation_router = APIRouter()

def get_autoloaded_classes() -> Dict[str, Dict[str, GeneratedQuestionClassType]]:
    base_package = 'question_generation.algo.algo_subclasses'
    base_path = Path(__file__).resolve().parent.parent / 'question_generation' / 'algo' / 'algo_subclasses'
    return autoload_classes(str(base_path), base_package)


@question_generation_router.get("/topics")
async def get_topics_route(autoloaded_classes: Dict[str, Dict[str, GeneratedQuestionClassType]] = Depends(get_autoloaded_classes)) -> List[str]:
    try:
        return list_topics(autoloaded_classes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@question_generation_router.get("/topics/{topic}/subtopics")
async def get_subtopics_route(topic: str, autoloaded_classes: Dict[str, Dict[str, GeneratedQuestionClassType]] = Depends(get_autoloaded_classes)) -> List[str]:
    try:
        return list_subtopics(autoloaded_classes, topic)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@question_generation_router.get("/topics/{topic}/subtopics/{subtopic}/queryables")
async def list_queryables_route(topic: str, subtopic: str, autoloaded_classes: Dict[str, Dict[str, GeneratedQuestionClassType]] = Depends(get_autoloaded_classes)) -> List[str]:
    try:
        return list_queryable(autoloaded_classes, topic, subtopic)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@question_generation_router.get("/queryable_classes")
async def get_queryable_classes_route(queryable_classes: Dict[str, Type[Queryable]]) -> List[str]:
    try:
        return list(queryable_classes.keys())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@question_generation_router.get("/topics/{topic}/subtopics/{subtopic}/queryables/{queryable}/variables")
async def list_variables_route(topic: str, subtopic: str, queryable: str, autoloaded_classes: Dict[str, Dict[str, GeneratedQuestionClassType]] = Depends(get_autoloaded_classes)) -> List[Dict[str, str]]:
    try:
        return list_variable(autoloaded_classes, topic, subtopic, queryable)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@question_generation_router.get("/quantifiables")
async def list_quantifiables_route() -> List[str]:
    try:
        subclasses = get_all_subclasses(Quantifiable)
        return [subclass.__name__ for subclass in subclasses]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@question_generation_router.post("/generate")
async def generate_route(request: GenerateQuestionRequest, autoloaded_classes: Dict[str, Dict[str, GeneratedQuestionClassType]] = Depends(get_autoloaded_classes)):
    results = []
    try:
        for _ in range(request.number_of_questions):
            generated_question = generate_question(
                autoloaded_classes, request.topic, request.subtopic,
                request.queryable, request.quantifiables,
                request.number_of_options, request.question_description,
            )

            if generated_question is None:
                raise HTTPException(status_code=500, detail="Failed to generate question.")

            results.append({
                **generated_question,
                "marks": request.marks,
            })
        return results
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))