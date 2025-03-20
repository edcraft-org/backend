from copy import deepcopy
from question_generation.algo.algo import Algo
from question_generation.input.input_subclasses.composite.list_type import ListInput
from question_generation.quantifiable.quantifiable_class import Quantifiable
from question_generation.queryable.queryable_subclasses.output import Output
from question_generation.queryable.queryable_subclasses.step import Step
from question_generation.question.question import Question


class InsertionSortClass(Algo, Question, Output, Step):
    def algo(self, input: ListInput[Quantifiable]):
        for i in range(1, len(input)):
            key = input[i]
            j = i - 1
            while j >= 0 and key < input[j]:
                input[j + 1] = input[j]
                j -= 1
            input[j + 1] = key
            self.step(input)
        self.output(input)
        return input