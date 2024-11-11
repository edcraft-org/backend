from copy import deepcopy
from typing import List
from question_generation.algo.algo import Algo
from question_generation.input.input_subclasses.composite.list_type import ListInput
from question_generation.quantifiable.quantifiable_class import Quantifiable
from question_generation.queryable.queryable_subclasses.output import Output
from question_generation.queryable.queryable_subclasses.step import Step
from question_generation.question.question import Question


class InsertionSortClass(Algo, Question, Output, Step):
    def algo(self, input: ListInput[Quantifiable]):
        ls = input.value()
        for i in range(1, len(ls)):
            key = ls[i]
            j = i - 1
            while j >= 0 and key.value() < ls[j].value():
                ls[j + 1] = ls[j]
                j -= 1
            ls[j + 1] = key
            self.step(deepcopy(ls))
        self.output(deepcopy(ls))
