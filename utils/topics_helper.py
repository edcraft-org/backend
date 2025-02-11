from typing import Dict, List
from question_generation.queryable.queryable_class import Queryable
from utils.classes_helper import get_subtopic_class
from utils.exceptions import handle_exceptions
from utils.types_helper import GeneratedQuestionClassType
from utils.user__code_helper import load_user_class

@handle_exceptions
def list_topics(autoloaded_classes: Dict[str, Dict[str, GeneratedQuestionClassType]]) -> List[str]:
    """Return a list of all topics."""
    return list(autoloaded_classes.keys())

@handle_exceptions
def list_subtopics(autoloaded_classes: Dict[str, Dict[str, GeneratedQuestionClassType]], topic: str) -> List[str]:
    """Return a list of all subtopics for a given topic."""
    if topic in autoloaded_classes:
        return list(autoloaded_classes[topic].keys())
    else:
        raise ValueError(f"Topic '{topic}' not found in autoloaded classes.")

@handle_exceptions
def list_queryable(autoloaded_classes: Dict[str, Dict[str, GeneratedQuestionClassType]], topic: str, subtopic: str) -> List[str]:
    cls = get_subtopic_class(autoloaded_classes, topic, subtopic)
    queryable_classes = [base.__name__ for base in cls.__bases__ if issubclass(base, Queryable)]
    return queryable_classes

@handle_exceptions
def list_user_queryable(userAlgoCode: str) -> List[str]:
    user_class = load_user_class(userAlgoCode)
    queryable_subclasses = [cls.__name__ for cls in user_class.__bases__ if issubclass(cls, Queryable) and cls is not Queryable and cls is not user_class]
    return queryable_subclasses
