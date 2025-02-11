import json
from pathlib import Path
import subprocess
from typing import Any, Dict, List, Type
import docker
from fastapi import APIRouter, Depends, HTTPException
from models import GenerateQuestionRequest
from models.question_generation import GenerateVariableRequest, UserQueryableRequest, VariableResponse
from question_generation.quantifiable.quantifiable_class import Quantifiable
from question_generation.queryable.queryable_class import Queryable
from utils.classes_helper import autoload_classes, get_subclasses_name
from utils.question_generation_helper import generate_question, generate_variable
from utils.variable_helper import list_algo_variable, list_queryable_variable
from utils.topics_helper import list_queryable, list_subtopics, list_topics, list_user_queryable
from utils.types_helper import GeneratedQuestionClassType

question_generation_router = APIRouter()
client = docker.from_env()

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

@question_generation_router.post("/user/queryables")
async def list_user_queryables_route(request: UserQueryableRequest) -> List[str]:
    try:
        return list_user_queryable(request.userAlgoCode)
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

@question_generation_router.get("/topics/{topic}/subtopics/{subtopic}/variables")
async def list_algo_variables_route(topic: str, subtopic: str, autoloaded_classes: Dict[str, Dict[str, GeneratedQuestionClassType]] = Depends(get_autoloaded_classes)) -> List[Dict[str, Any]]:
    try:
        return list_algo_variable(autoloaded_classes, topic, subtopic)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@question_generation_router.get("/topics/{topic}/subtopics/{subtopic}/queryables/{queryable}/variables")
async def list_queryable_variables_route(topic: str, subtopic: str, queryable: str, autoloaded_classes: Dict[str, Dict[str, GeneratedQuestionClassType]] = Depends(get_autoloaded_classes)) -> List[Dict[str, Any]]:
    try:
        return list_queryable_variable(autoloaded_classes, topic, subtopic, queryable)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@question_generation_router.get("/quantifiables")
async def list_quantifiables_route() -> List[str]:
    try:
        return get_subclasses_name(Quantifiable)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@question_generation_router.post("/generate_variable")
async def generate_variable_route(request: GenerateVariableRequest, autoloaded_classes: Dict[str, Dict[str, GeneratedQuestionClassType]] = Depends(get_autoloaded_classes)) -> VariableResponse:
    try:
        result = generate_variable(
            autoloaded_classes,
            request.topic,
            request.subtopic,
            request.arguments,
            request.element_type,
            request.subclasses,
            request.question_description,
        )
        result['context'] = {key: str(value) for key, value in result['context'].items()}
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@question_generation_router.post("/generate")
async def generate_route(request: GenerateQuestionRequest):
    try:
        input_data = {
            "request": request.model_dump(),
        }
        input_json = json.dumps(input_data)
        result = subprocess.run(
            [
                "docker", "run", "--rm", "-i",
                "sandbox_image"
            ],
            input=input_json,
            capture_output=True,
            text=True
        )
        json_start = result.stdout.rfind('{"result"')
        if json_start != -1:
            valid_json_str = result.stdout[json_start:]
            output = json.loads(valid_json_str)
            return output['result']
        else:
            return {"error": "No valid JSON found in the output"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @question_generation_router.post("/generate")
# async def generate_route(request: GenerateQuestionRequest, autoloaded_classes: Dict[str, Dict[str, GeneratedQuestionClassType]] = Depends(get_autoloaded_classes)):
#     try:
#         return generate_question(request, autoloaded_classes)
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))