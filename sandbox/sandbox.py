from pathlib import Path
import sys
import json
from typing import Dict
from models.question_generation import GenerateQuestionRequest
from utils.classes_helper import autoload_classes
from utils.types_helper import GeneratedQuestionClassType
from utils.question_generation_helper import generate_question


def get_autoloaded_classes() -> Dict[str, Dict[str, GeneratedQuestionClassType]]:
    try:
        base_package = 'question_generation.algo.algo_subclasses'
        base_path = Path(__file__).resolve().parent / 'question_generation' / 'algo' / 'algo_subclasses'
        return autoload_classes(str(base_path), base_package)
    except Exception as e:
        return str(e)


def execute_user_code(request: GenerateQuestionRequest):
    try:
        autoloaded_classes = get_autoloaded_classes()
        result = generate_question(request, autoloaded_classes)
        return result
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    input_data = json.loads(sys.stdin.read())
    request = GenerateQuestionRequest(**input_data["request"])
    result = execute_user_code(request)
    print(json.dumps({"result": result}))