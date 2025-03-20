from typing import Any, Dict, List, Optional, Type
from question_generation.queryable.queryable_class import Queryable
from utils.classes_helper import get_input_class, get_subtopic_class
from utils.exceptions import handle_exceptions
from utils.types_helper import GeneratedQuestionClassType
from utils.user__code_helper import load_input_class, load_user_class

@handle_exceptions
def list_keys(loaded_classes: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Return a nested dictionary of all folder and file names without class values."""

    def build_nested_dict(d: Dict[str, Any], key: Any, value: Any) -> None:
        """Helper function to build a nested dictionary, keeping only key names."""
        if isinstance(value, dict):
            d[key] = {}
            for subkey, subvalue in value.items():
                build_nested_dict(d[key], subkey, subvalue)
        else:
            d[key] = {}

    nested_dict = {}
    for folder, subfolders in loaded_classes.items():
        build_nested_dict(nested_dict, folder, subfolders)
    return nested_dict


@handle_exceptions
def list_queryable(autoloaded_classes: Dict[str, Dict[str, GeneratedQuestionClassType]], topic: str, subtopic: str) -> List[str]:
    cls = get_subtopic_class(autoloaded_classes, topic, subtopic)
    queryable_classes = [base.__name__ for base in cls.__bases__ if issubclass(base, Queryable)]
    return queryable_classes

@handle_exceptions
def list_user_queryable(userAlgoCode: str, userEnvCode: Optional[List[str]] = None) -> List[str]:
    user_class = load_user_class(userAlgoCode, userEnvCode=userEnvCode)
    queryable_subclasses = [cls.__name__ for cls in user_class.__bases__ if issubclass(cls, Queryable) and cls is not Queryable and cls is not user_class]
    return queryable_subclasses

@handle_exceptions
def list_input_queryable(input_path: Dict[str, Any], input_classes: Dict[str, Dict[str, Type]]) -> List[str]:
    input_class = get_input_class(input_path, input_classes)
    queryable_subclasses = [cls.__name__ for cls in input_class.__bases__ if issubclass(cls, Queryable)]
    return queryable_subclasses

@handle_exceptions
def list_user_input_queryable(userEnvCode:str) -> List[str]:
    user_class = load_input_class(userEnvCode)
    queryable_subclasses = [cls.__name__ for cls in user_class.__bases__ if issubclass(cls, Queryable) and cls is not Queryable and cls is not user_class]
    return queryable_subclasses
