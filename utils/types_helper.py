from typing import Type, Union

from question_generation.algo.algo import Algo
from question_generation.queryable.queryable_class import Queryable
from question_generation.question.question import Question

GeneratedQuestionClassType = Union[Type[Algo], Type[Question], Type[Queryable]]
