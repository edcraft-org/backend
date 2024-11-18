from copy import deepcopy
from question_generation.algo.algo import Algo
from question_generation.input.input_subclasses.composite.list_type import ListInput
from question_generation.quantifiable.quantifiable_class import Quantifiable
from question_generation.queryable.queryable_subclasses.output import Output
from question_generation.queryable.queryable_subclasses.step import Step
from question_generation.question.question import Question


class BubbleSortClass(Algo, Question, Output, Step):
    def __init__(self):
        super().__init__()

    def algo(self, input: ListInput[Quantifiable]):
        ls = input.value()
        n = len(ls)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if ls[j] > ls[j + 1]:
                    ls[j], ls[j + 1] = ls[j + 1], ls[j]
                    swapped = True
            self.step(deepcopy(ls))
            if not swapped:
                break
        self.output(deepcopy(ls))
